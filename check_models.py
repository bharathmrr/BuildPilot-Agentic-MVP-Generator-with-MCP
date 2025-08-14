import ollama

try:
    client = ollama.Client()
    models = "gemma3:1b-it-qat"
    
    print("Available Ollama models:")
    print("-" * 30)
    
    # Handle different response formats
    if isinstance(models, dict):
        if 'models' in models:
            for model in models['models']:
                # Try different possible keys
                if isinstance(model, dict):
                    name = model.get('name', model.get('model', 'Unknown'))
                    print(f"  {name}")
                else:
                    print(f"  {model}")
        else:
            print("Response format:", models)
    else:
        print("Unexpected response type:", type(models))
        
    print("\nTo use a model, update the 'model' variable in app_simple.py")
    print("For example: model = 'llama2' or model = 'mistral'")
    
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    print("\nMake sure Ollama is running:")
    print("  ollama serve")
    print("\nThen pull a model:")
    print("  ollama pull llama2")