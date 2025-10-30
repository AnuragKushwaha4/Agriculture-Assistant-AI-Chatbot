package com.example.Chatbot.Interface.Controller;

import com.example.Chatbot.Interface.Model.ChatMessage;
import com.example.Chatbot.Interface.Security.JwtUtil;
import com.example.Chatbot.Interface.Services.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

@RestController
public class ChatController {
    @Autowired
    JwtUtil jwtUtil;
    @Autowired
    ChatService chatService;

    @GetMapping("/chats")
    public Set<String> getChats(@RequestHeader("Authorization") String token){
        String username = jwtUtil.validateAndGetClaims(token.substring(7)).getSubject();
        List<String> chats = chatService.getChats(username);
        Set<String> distinctChat = new HashSet<>(chats);
        System.out.println(distinctChat);
        return distinctChat;
    }

    @GetMapping("/message")
    public ResponseEntity<?> getMessages(@RequestParam String query,
                                         @RequestHeader("Authorization") String token){
        String username = jwtUtil.validateAndGetClaims(token.substring(7)).getSubject();
        System.out.println("sending something");
        return chatService.getMessages(query, username);
    }

    @PostMapping("/message")
    public ResponseEntity<?> saveMessage(@RequestBody ChatMessage message,
                                         @RequestHeader("Authorization") String token){
        String username = jwtUtil.validateAndGetClaims(token.substring(7)).getSubject();
        message.setUsername(username);
        System.out.println(message.getSender());
        return chatService.saveMessage(message);
    }
}
