package com.example.Chatbot.Interface.Services;

import com.example.Chatbot.Interface.Model.ChatMessage;
import com.example.Chatbot.Interface.Repository.ChatRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class ChatService {
    @Autowired
    ChatRepository repo;

    public ResponseEntity<?> saveMessage(ChatMessage chatMessage){
        return ResponseEntity.ok(repo.save(chatMessage));
    }

    public ResponseEntity<?> getMessages(String chatRoomId, String username){
        if(repo.findByQuery(chatRoomId, username).isEmpty()){return ResponseEntity.badRequest().body("Chat not found");}
        return ResponseEntity.ok(repo.findByQuery(chatRoomId, username));
    }

    public List<String> getChats(String username){
        return repo.findByUsername(username);
    }
}
