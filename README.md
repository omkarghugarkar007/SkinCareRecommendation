# SkinCare Recommendation System

A powerful AI-powered skincare recommendation system that helps users find the perfect skincare products based on their needs and preferences.

## 🚀 Features

- **Smart Query Classification**: Automatically detects if the user is looking for product recommendations or general information
- **Interactive Q&A**: Asks relevant follow-up questions to refine product recommendations
- **RAG-Powered Responses**: Provides accurate, context-aware answers using Retrieval-Augmented Generation
- **Product Recommendations**: Suggests skincare products based on user's needs and preferences
- **Modern Web Interface**: Clean, responsive UI built with Streamlit

## 🛠️ Prerequisites

- Python 3.8+
- pip (Python package manager)
- OpenAI API key

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skincare-recommendation-system.git
   cd skincare-recommendation-system
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Start the application**
   ```bash
   # Start the FastAPI backend
   uvicorn api:app --reload --port 8000

   # In a new terminal, start the Streamlit frontend
   streamlit run app.py
   ```

6. **Access the application**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 📂 Project Structure

```
skincare-recommendation-system/
├── api.py               # FastAPI backend
├── app.py               # Streamlit frontend
├── utils.py             # Core functionality
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # This file
```

## 🌟 API Endpoints

- `POST /api/intent` - Classify user query intent
- `POST /api/recommendation/questions` - Get follow-up questions for recommendations
- `POST /api/recommendation/final` - Get final recommendation based on user input
- `POST /api/rag` - Get RAG-based responses
- `POST /api/products` - Search for products (requires implementation)

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- Streamlit for the amazing UI framework
- FastAPI for the high-performance backend
- The open-source community for inspiration and support
