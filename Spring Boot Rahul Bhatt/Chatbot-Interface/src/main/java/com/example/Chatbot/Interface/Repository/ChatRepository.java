package com.example.Chatbot.Interface.Repository;

import com.example.Chatbot.Interface.Model.ChatMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatRepository extends JpaRepository<ChatMessage, Long> {
    @Query("SELECT c FROM ChatMessage c WHERE c.query = :query AND c.username = :name")
    List<ChatMessage> findByQuery(@Param("query") String query,
                                  @Param("name") String username);

    @Query("SELECT c.query FROM ChatMessage c WHERE c.username = :name")
    List<String> findByUsername(@Param("name") String username);
}
