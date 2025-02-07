from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from translatepy import Translator
from a_rtchat.models import ChatGroup
from .forms import ChatmessageCreateForm, NewGroupForm, ChatRoomEditForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect  # Enforces CSRF protection
@require_POST  # Ensures only POST requests are allowed
def translate_message(request):
    try:
        data = json.loads(request.body)
        text = data.get("text")
        target_language = data.get("target_language")

        if text and target_language:
            translator = Translator()
            translated_text = translator.translate(text, target_language).result
            print(translated_text,"===========", target_language)
            return JsonResponse({"translated_text": translated_text})

        return JsonResponse({"error": "Invalid request"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def chat_view(request, chatroom_name = 'public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
           if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
           else:
                messages.warning(request, "You need to verify your email to join the chat!")
                return redirect('profile-settings')

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                "message": message,
                "user": request.user,
            }
            return render(request, "a_rtchat/partials/chat_message_p.html", context)

    context = {
            'chat_messages': chat_messages,
            'form': form,
            'other_user': other_user,
            'chatroom_name': chatroom_name,
            'chat_group': chat_group,
        }
    return render(request, 'a_rtchat/chat.html', context=context)


def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
                print("Chatroom: ", chatroom.members.all)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)


@login_required
def create_groupchat(request):
    form = NewGroupForm(request.POST)
    if form.is_valid():
        new_groupchat = form.save(commit=False)
        new_groupchat.admin = request.user
        new_groupchat.save()
        new_groupchat.members.add(request.user)
        return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form,
    }
    return render(request, 'a_rtchat/create_groupchat.html', context)

@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)
    if request.user != chat_group.admin:
        raise Http404
    form = ChatRoomEditForm(instance=chat_group)

    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            print("Heee")
            form.save()

            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)
            return redirect('chatroom', chatroom_name)

    context = {
        'form': form,
        'chat_group': chat_group
    }
    return render(request, 'a_rtchat/chatroom_edit.html', context)

@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)
    if request.user != chat_group.admin:
        raise Http404
    if request.method == 'POST':
        chat_group.delete()
        messages.success(request, "You have successfully deleted your chat room.")
        return redirect('home')
    return render(request, 'a_rtchat/chatroom_delete.html', {'chat_group': chat_group})

