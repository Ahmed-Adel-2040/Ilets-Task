import language_check
lang_tool = language_check.LanguageTool("en-US")
text = "A sentence with a error in the Hitchhiker’s Guide tot he Galaxy. Ahmed Adel are big enginee And data analysite"
matches = lang_tool.check(text)
print('Number of mistakes',len(matches))
for mistake in matches:
    print(mistake)