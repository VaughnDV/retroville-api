from retroville.providers.voice import get_voice_provider


def generate_token(identity) -> str:
    return get_voice_provider().access_token(str(identity))
