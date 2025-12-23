from deep_translator import GoogleTranslator
import polib

po = polib.pofile('locale/en/LC_MESSAGES/django.po')

for entry in po:
    if entry.msgid.strip() and not entry.msgstr:  
        try:
            entry.msgstr=entry.msgid
            print(entry.msgstr)
            
        except Exception as e:
            print(f"Xato: {entry.msgid} -> {e}")

po.save()
print("Tarjima tugadi!")


