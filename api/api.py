from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return {"message": "Hello, world!"}

@api.post("/guess")
def make_guess(request):
    print(f"Received guess: {request.POST.get('guess')}")
    return {"status": "Guess received", "your_guess": request.POST.get('guess')}