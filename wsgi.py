from src.server import create_app

def run():
    application = create_app()
    application.run()

if __name__ == "__main__":
    run()