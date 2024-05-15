import os

fp = open('JA.MO', 'rb')

# ヘッダ項目の読み取りと表示
magic_number = fp.read(4)
file_format_revision = fp.read(4)
number_of_strings = fp.read(4)
offset_of_table_with_original_strings = fp.read(4)
offset_of_table_with_translation_strings = fp.read(4)
size_of_hash_table = fp.read(4)
offset_of_hash_table = fp.read(4)

print('number_of_strings: {}'.format(number_of_strings.hex()))
print('offset_of_table_with_original_strings: {}'.format(offset_of_table_with_original_strings.hex()))
print('offset_of_table_with_translation_strings: {}'.format(offset_of_table_with_translation_strings.hex()))
print('size_of_hash_table: {}'.format(size_of_hash_table.hex()))
print('offset_of_hash_table: {}'.format(offset_of_hash_table.hex()))

# messageの総数を表示
num = int.from_bytes(number_of_strings, 'little')
print('size of messages: {}'.format(num))
# message idの取得
cursor = int.from_bytes(offset_of_table_with_original_strings, 'little')
fp.seek(cursor, os.SEEK_SET)
message_id_dict = {} # message id格納用のdict
for i in range(num):
    message_strings = fp.read(8)
    message_strings_length = int.from_bytes(message_strings[0:4], 'little')
    message_strings_offset = int.from_bytes(message_strings[4:8], 'little')

    fp.seek(message_strings_offset, os.SEEK_SET)
    message_id = fp.read(message_strings_length).decode()
    # print('message id = {}'.format(message_id))
    message_id_dict[i] = message_id
    cursor = cursor + 8
    fp.seek(cursor, os.SEEK_SET)

# messageの取得
cursor = int.from_bytes(offset_of_table_with_translation_strings, 'little')
fp.seek(cursor, os.SEEK_SET)
message_translation_dict = {} # message translation格納用のdict
for i in range(num):
    message_strings = fp.read(8)
    message_strings_length = int.from_bytes(message_strings[0:4], 'little')
    message_strings_offset = int.from_bytes(message_strings[4:8], 'little')

    fp.seek(message_strings_offset, os.SEEK_SET)
    message_translation = fp.read(message_strings_length).decode()
    # print('message translation = {}'.format(message_translation))
    message_translation_dict[i] = message_translation
    cursor = cursor + 8
    fp.seek(cursor, os.SEEK_SET)

# message idとmessage translationの結合
print('message ids: {}'.format(len(message_id_dict)))
print('message translations: {}'.format(len(message_translation_dict)))

for i in range(num):
    print('msgid "{}"'.format(message_id_dict[i]))
    print('msgstr "{}"'.format(message_translation_dict[i]))
    print('')
    # print('{}, {}'.format(message_id_dict[i], message_translation_dict[i]))
#size = (int.from_bytes(number_of_strings, 'little') - 1) * 8
#dump = fp.read(size)
#print('string size = {}'.format(size))
#print('{}: {}'.format(dump[0:4].hex(), dump[4:8].hex()))
#
#fp.seek(int.from_bytes(dump[4:8], 'little'), os.SEEK_SET)
#aaa = fp.read(int.from_bytes(dump[0:4], 'little'))
#print(aaa.decode())
fp.close()
