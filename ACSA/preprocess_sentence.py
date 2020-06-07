import re
import string
import unicodedata as ud

from vncorenlp import VnCoreNLP

annotator = VnCoreNLP("./VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx500m')

def normalize_text(vncorenlp,text):
    text = ud.normalize('NFC', text)
    #Remove các ký tự kéo dài: vd: đẹppppppp
    text = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), text, flags=re.IGNORECASE)

    #Chuẩn hóa tiếng Việt, xử lý emoj, chuẩn hóa tiếng Anh, thuật ngữ
    replace_list = {
        'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé','ỏe': 'oẻ',
        'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ','ụy': 'uỵ', 'uả': 'ủa',
        'ả': 'ả', 'ố': 'ố', 'u´': 'ố','ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
        'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề','ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
        'ẻ': 'ẻ', 'àk': u' à ','aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ','ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á',
        #Quy các icon về 2 loại emoj: Tích cực hoặc tiêu cực
        "👹": " tích cực ", "👻": " tích cực ", "💃": " tích cực ",'🤙': ' tích cực ', '👍': ' tích cực ',
        "💄": " tích cực ", "💎": " tích cực ", "💩": " tích cực ","😕": " tiêu cực ", "😱": " tiêu cực ", "😸": "tích cực",
        "😾": " tiêu cực ", "🚫": " tiêu cực ",  "🤬": " tiêu cực ","🧚": " tích cực ", "🧡": " tích cực ",'🐶':' tích cực ',
        '👎': ' tiêu cực ', '😣': ' tiêu cực ','✨': ' tích cực ', '❣': ' tích cực ','☀': ' tích cực ',':D': ' tích cực ',
        '♥': ' tích cực ', '🤩': ' tích cực ', 'like': ' tích cực ', '💌': ' tích cực ',
        '🤣': ' tích cực ', '🖤': ' tích cực ', '🤤': ' tích cực ', ':(': ' tiêu cực ', '😢': ' tiêu cực ',':\'(': ' tiêu cực ',
        '❤': ' tích cực ', '😍': ' tích cực ', '😘': ' tích cực ', '😪': ' tiêu cực ', '😊': ' tích cực ',
        '?': ' ? ', '😁': ' tích cực ', '💖': ' tích cực ', '😟': ' tiêu cực ', '😭': ' tiêu cực ',
        '💯': ' tích cực ', '💗': ' tích cực ', '♡': ' tích cực ', '💜': ' tích cực ', '🤗': ' tích cực ',
        '^^': ' tích cực ', '😨': ' tiêu cực ', '☺': ' tích cực ', '💋': ' tích cực ', '👌': ' tích cực ',
        '😖': ' tiêu cực ', '😀': ' tích cực ', ':((': ' tiêu cực ', '😡': ' tiêu cực ', '😠': ' tiêu cực ',
        '😒': ' tiêu cực ', '🙂': ' tích cực ', '😏': ' tiêu cực ', '😝': ' tích cực ', '😄': ' tích cực ',
        '😙': ' tích cực ', '😤': ' tiêu cực ', '😎': ' tích cực ', '😆': ' tích cực ', '💚': ' tích cực ',
        '✌': ' tích cực ', '💕': ' tích cực ', '😞': ' tiêu cực ', '😓': ' tiêu cực ', '️🆗️': ' tích cực ',
        '😉': ' tích cực ', '😂': ' tích cực ', ':v': '  tích cực ', '=))': '  tích cực ', '😋': ' tích cực ',
        '💓': ' tích cực ', '😐': ' tiêu cực ', ':3': ' tích cực ', '😫': ' tiêu cực ', '😥': ' tiêu cực ',
        '😃': ' tích cực ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' tích cực ', '🤝': ' tích cực ', '🎈': ' tích cực ',
        '😗': ' tích cực ', '🤔': ' tiêu cực ', '😑': ' tiêu cực ', '🔥': ' tiêu cực ', '🙏': ' tiêu cực ',
        '🆗': ' tích cực ', '😻': ' tích cực ', '💙': ' tích cực ', '💟': ' tích cực ',
        '😚': ' tích cực ', '❌': ' tiêu cực ', '👏': ' tích cực ', ';)': ' tích cực ', '<3': ' tích cực ',
        '🌝': ' tích cực ',  '🌷': ' tích cực ', '🌸': ' tích cực ', '🌺': ' tích cực ',
        '🌼': ' tích cực ', '🍓': ' tích cực ', '🐅': ' tích cực ', '🐾': ' tích cực ', '👉': ' tích cực ',
        '💐': ' tích cực ', '💞': ' tích cực ', '💥': ' tích cực ', '💪': ' tích cực ',
        '💰': ' tích cực ',  '😇': ' tích cực ', '😛': ' tích cực ', '😜': ' tích cực ',
        '🙃': ' tích cực ', '🤑': ' tích cực ', '🤪': ' tích cực ','☹': ' tiêu cực ',  '💀': ' tiêu cực ',
        '😔': ' tiêu cực ', '😧': ' tiêu cực ', '😩': ' tiêu cực ', '😰': ' tiêu cực ', '😳': ' tiêu cực ',
        '😵': ' tiêu cực ', '😶': ' tiêu cực ', '🙁': ' tiêu cực ','👍🏻': ' tích cực ',
        '🍤': '', '😬': '', '🔹': '','🙆🏼': '', '🍛': '', '🍗': '','=))': '  tích cực ','=)))': '  tích cực ',
        '🚹': '', '🐟': '', '🍮': '','😅': '', '💔': '', '🙋': '','☔':'','✔':'','🤘':'',
        '🔵': '', '👇': '', '😽': '','🍡': '', '🍢': '', '✅': '','▶':'','•':'','♻':'',
        '🍣': '', '🍲': '', '🍜': '','🙀': '', '🌋': '', '🎊': '','ㅁ':'','ㅠㅠ':'',
        '⛔': '', '🦀': '', '📝': '','🏠': '', '🐷': '', '🙄': '',
        '🎀': '', '💘': '', '☕': '',
        #Chuẩn hóa 1 số sentiment words/English words
        ':))': '  tích cực ', ':)': ' tích cực ', 'ô kêi': ' ok ', 'okie': ' ok ', ' o kê ': ' ok ',
        'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', ' oke ':  ' ok ',' okay':' ok ','okê':' ok ',
        ' tks ': u' cám ơn ', 'thks': u' cám ơn ', 'thanks': u' cám ơn ', 'ths': u' cám ơn ', 'thank': u' cám ơn ',
        '⭐': 'star ', '*': 'star ', '🌟': 'star ', '🎉': u' tích cực ',
        'kg ': u' không ','not': u' không ', u' kg ': u' không ', '"k ': u' không ',' kh ':u' không ','kô':u' không ','hok':u' không ',' kp ': u' không phải ',u' kô ': u' không ', '"ko ': u' không ', u' ko ': u' không ', u' k ': u' không ', 'khong': u' không ', u' hok ': u' không ',
        'he he': ' tích cực ','hehe': ' tích cực ','hihi': ' tích cực ', 'haha': ' tích cực ', 'hjhj': ' tích cực ',
        ' lol ': ' tiêu cực ',' cc ': ' tiêu cực ','cute': u' dễ thương ','huhu': ' tiêu cực ', ' vs ': u' với ', 'wa': ' quá ', 'wá': u' quá', 'j': u' gì ', '“': ' ',
        ' sz ': u' cỡ ', 'size': u' cỡ ', u' đx ': u' được ', 'dk': u' được ', 'dc': u' được ', 'đk': u' được ',
        'đc': u' được ','authentic': u' chuẩn chính hãng ',u' aut ': u' chuẩn chính hãng ', u' auth ': u' chuẩn chính hãng ', 'thick': u' tích cực ', 'store': u' cửa hàng ',
        'shop': u' cửa hàng ', 'sp': u' sản phẩm ', 'gud': u' tốt ','god': u' tốt ','wel done':' tốt ', 'good': u' tốt ', 'gút': u' tốt ',
        'sấu': u' xấu ','gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt', 'bt': u' bình thường ',
        'time': u' thời gian ', 'qá': u' quá ', u' ship ': u' giao hàng ', u' m ': u' mình ', u' mik ': u' mình ',
        'ể': 'ể', 'product': 'sản phẩm', 'quality': 'chất lượng','chat':' chất ', 'excelent': 'hoàn hảo', 'bad': 'tệ','fresh': ' tươi ','sad': ' tệ ',
        'date': u' hạn sử dụng ', 'hsd': u' hạn sử dụng ','quickly': u' nhanh ', 'quick': u' nhanh ','fast': u' nhanh ','delivery': u' giao hàng ',u' síp ': u' giao hàng ',
        'beautiful': u' đẹp tuyệt vời ', u' tl ': u' trả lời ', u' r ': u' rồi ', u' shopE ': u' cửa hàng ',u' order ': u' đặt hàng ',
        'chất lg': u' chất lượng ',u' sd ': u' sử dụng ',u' dt ': u' điện thoại ',u' nt ': u' nhắn tin ',u' tl ': u' trả lời ',u' sài ': u' xài ',u'bjo':u' bao giờ ',
        'thik': u' thích ',u' sop ': u' cửa hàng ', ' fb ': ' facebook ', ' face ': ' facebook ', ' very ': u' rất ',u'quả ng ':u' quảng  ',
        'dep': u' đẹp ',u' xau ': u' xấu ','delicious': u' ngon ', u'hàg': u' hàng ', u'qủa': u' quả ',
        'iu': u' yêu ','fake': u' giả mạo ', 'trl': 'trả lời', '><': u' tích cực ',
        ' por ': u' tệ ',' poor ': u' tệ ', 'ib':u' nhắn tin ', 'rep':u' trả lời ',u'fback':' feedback ','fedback':' feedback ',
        #dưới 3* quy về 1*, trên 3* quy về 5*
        '6 sao': ' 5star ','6 star': ' 5star ', '5star': ' 5star ','5 sao': ' 5star ','5sao': ' 5star ',
        'starstarstarstarstar': ' 5star ', '1 sao': ' 1star ', '1sao': ' 1star ','2 sao':' 1star ','2sao':' 1star ',
        '2 starstar':' 1star ','1star': ' 1star ', '0 sao': ' 1star ', '0star': ' 1star ',}

    for k, v in replace_list.items():
        text = text.replace(k, v)
    
    upper_char = r"[AĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴA-Z]"
    p_string = r"(\S)(" + upper_char + r")"
    pattern = re.compile(p_string)
    text = re.sub(pattern, r"\1 \2", text)
    text = re.sub(r"(\d+)([^\d\s]+)", r"\1 \2", text)
    text = re.sub(r"([^\d\s]+)(\d+)", r"\1 \2", text)
    text = re.sub(r"\d+\s*(k|đ|Đ|d)\d*\s*", r" giá cả ", text)
    text = re.sub(r"#\S+", r" hagtag ", text)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    # text = re.sub(r"\d", r"", text)
    # chuyen punctuation thành space
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    text = text.translate(translator)
    
    # Chuyển thành chữ thường
    text = text.lower()
    sens = vncorenlp.tokenize(text)

    tokens = sens[0]

    text = u' '.join(tokens)

    #remove nốt những ký tự thừa thãi
    text = text.replace(u'"', u' ')
    text = text.replace(u'️', u'')
    text = text.replace('🏻','')
    return text

# text = normalize_text(annotator, "- Các bạn nhìn cái chảo này có to. không 🙄🙄🙄- Trên. hình thấy nó cũng to mà ra bên ngoài nó bé tí tẹo tèo teo í 😅😅😅😅- Mà nhìn hoàng tráng lắm - Ăn là no muốn lăn luôn hahaaa - Cái này từ hồi mình ở Hà Nội đã thèm thuồng và vẫn chưa có cơ hội thử thì vô Sài Gòn có quán bánh mì chảo đậm chất Hà Nội đây 👍🏼👍🏼👍🏼- Thêm địa điểm cho mấy bạn nên đi thử nhé - Không thất vọng đâu vì nó khá ngon hê hê")
# print(text)
# annotator.close()