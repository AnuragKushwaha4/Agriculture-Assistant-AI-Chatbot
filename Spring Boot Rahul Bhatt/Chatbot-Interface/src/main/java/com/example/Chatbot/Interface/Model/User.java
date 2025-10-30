package com.example.Chatbot.Interface.Model;
import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    private String username;
    private String password;

    // getters & setters
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
