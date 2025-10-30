🌾 AI-Powered Agricultural Research Assistant

An AI-integrated platform built to assist agriculture students, researchers, and scientists in finding, understanding, and analyzing agricultural research papers.
The system combines Next.js (frontend), Spring Boot (backend), and LangChain-powered AI to deliver intelligent insights, secure user management, and an interactive chat interface.

🚀 Features

🧠 AI & Research Assistant

Fetches latest agricultural research papers using the OpenAlex API.

Provides context-based, summarized insights from research documents.

Answers domain-specific queries through LLM (Llama 3.3 via Groq API).

🧩 System Architecture

Frontend (Next.js) — User-friendly chat interface, real-time interaction, and research visualization.

Backend (Spring Boot) — Handles authentication, user registration, chat history management, and API routing.

AI Microservice (Flask + LangChain) — Core AI logic for retrieval, summarization, and context-based Q&A.

🔐 Authentication & Security

JWT-based authentication for secure API communication.

Encrypted password storage and secure session handling.

Role-based access for researchers, students, and admins.

💬 User Features

User registration and login.

Personalized dashboard with saved chats and research history.

Instant query responses powered by LangChain + Groq.

Smart context retrieval from Chroma vector database.

🧰 Tech Stack
Layer Technology Used
Frontend--Next.js, React, Tailwind CSS
Backend --Spring Boot, Java, MySQL
AI Engine --Flask, LangChain, Chroma, Hugging Face, Groq
Database -- MySQL (User Data), ChromaDB (Vector Storage)
APIs -- OpenAlex API (Research Papers), Custom AI Endpoints
Authentication -- JWT, Spring Security
