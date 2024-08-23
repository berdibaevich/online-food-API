from string import ascii_letters

from rest_framework import serializers


def validate_username(username):
    if len(username) <= 2:
        raise serializers.ValidationError("Kiritilgen mag'liwmat keminde 2 characterden kem bolmawi kerek. Misali (Wade)")
    
    if username.isdigit():
        raise serializers.ValidationError(f"{username}, bunday qilip saqlap aliwdin' ilaji joq blaaa bratan. Misali (Wade13, Wade 13 yamasa 13 Wade).")

    # TOMENDE WAQTINSHA MUZDA OK 
    # letters = ascii_letters #abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

    # for s in value:
    #     if len(s.strip(letters)) != 0:
    #         raise serializers.ValidationError("Username di tek g'ana alphabet tu'rinde kiritin'.")