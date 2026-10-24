"""글 다듬기 전후 검사.

python -I check.py 원문.txt 고친글.txt [--keep 지킬낱말.txt]   전후 대조
python -I check.py 원문.txt 판1.txt 판2.txt 판3.txt    여러 판 비교 표
python -I check.py 원문.txt                     원문의 티 문장 비율과 문턱값을 넘은 꼴

결과는 표준 출력으로 낸다. 판정은 하지 않고 살펴볼 곳만 보인다.
"""
import difflib
import re
import sys
import unicodedata
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

# 고친 글에서 늘면 안 되는 꼴
GROW = [
    ("연결어미 뒤 쉼표", r"(?:고|며|지만|면서|아서|어서|는데),"),
    ("대비 'A가 아니라 B'", r"[가이] 아니라|것이 아니라|것은 아니|라기보다"),
    ("'더 이상 ~않'", r"더\s?이상[^.!?\n]{0,25}(?:않|아니|없|못)"),
    ("'결국'", r"결국"),
    ("'~하는 이유다'", r"이유(?:다|입니다|이다|예요|이에요)[.!]"),
    ("분열문 '핵심은·필요한 것은'", r"(?:필요한|중요한)\s?(?:것은|건)|핵심은|관건은"),
    ("상투구", r"기록적인\s?성과|괄목할\s?만한|로\s?평가(?:된|받)|주목받|크게\s?기여|중요한\s?역할|시사하는\s?바|의미가\s?크|자리매김"),
    ("격식 올림 '하였'", r"하였"),
    ("새 양보 '다만·물론'", r"(?:^|[.!?]\s)(?:다만|물론)[ ,]"),
    ("이중 부정 '작지 않다·결코'", r"(?:작지|적지|가볍지|만만치|녹록지|간단치)\s?않|결코"),
    ("'~에 그치지 않는다·~에 가깝다'", r"그치지\s?않|에\s?가깝"),
    ("'그만큼'", r"그만큼"),
    ("'함의·곱씹다·읽어 내다'", r"함의|곱씹|읽어\s?내"),
    ("결말 '지금이 ~할 때'", r"(?:지금|이제)[이은는가]?\s[^.!?\n]{0,50}때(?:다|입니다|이다)"),
    ("돌려 말하기 '진행·수행·실시'", r"(?:진행|수행|실시)(?:하|했|한|해|할|되|됐)"),
    ("당위 '~해야'", r"[가-힣]야\s?(?:한다|합니다|할|해요|하고|하며|겠)"),
]
# 고친 글에서 줄면 서법이 바뀌었을 수 있는 꼴
KEEP = [
    ("추정·가능", r"것\s?같|(?:로|으로)\s?보(?:인|입|여)|듯하|듯합|판단(?:된|됩)|여겨|가능성|배제할\s?수\s?없|여지가\s?있|[가-힣]\s수\s?(?:도\s?)?있"),
    ("당위", r"[가-힣]야\s?(?:한다|합니다|할|해요|하고|하며|겠)|필요가\s?있|필요하|시급하|바람직하|요구된|요구됩"),
]
# 원문에서 이 횟수를 넘을 때만 고칠 꼴 (이름, 꼴, 단위, 문턱)
DENSE = [
    ("~에 대해·~에 대한", r"에\s?대해|에\s?대한", "문단", 3),
    ("~를 통해", r"[을를]\s?통해|[을를]\s?통하여", "문단", 3),
    ("~을 위해", r"[을를]\s?위해|[을를]\s?위한", "문단", 3),
    ("문두 또한·따라서·즉·나아가·아울러", r"(?:^|[.!?]\s)(?:또한|따라서|즉|나아가|아울러|게다가|더욱이)[ ,]", "문단", 3),
    ("~되고 있다·~지고 있다", r"[되지]고\s?있", "문단", 3),
    ("이는·이 점에서", r"(?:^|[.!?]\s)(?:이는|이 점에서|이 관점에서)", "문단", 3),
    ("~할 수 있다", r"[가-힣]\s수\s?(?:도\s?)?있", "글", 4),
    ("연결어미 뒤 쉼표(에세이·블로그만, 칼럼·보고서·설명문은 무시)", r"(?:고|며|지만|면서|아서|어서|는데),", "글", 6),
    ("대비 'A가 아니라 B'", r"[가이] 아니라|것이 아니라|것은 아니", "글", 2),
    ("논리 결산 '결국'", r"결국", "글", 2),
    ("'즉'", r"(?:^|\s)즉[, ]", "글", 3),
    ("따옴표 강조", r"[\"“'‘][^\"”'’\n]{1,15}[\"”'’]", "글", 6),
    ("단순한 X를 넘어", r"단순한?\s.{0,15}[을를]\s?넘어", "글", 1),
    ("이중 조사 ~에서의·~으로의", r"에서의|에로의|으로의|에의|로부터의", "글", 1),
    ("분열문 '핵심은·필요한 것은'", r"(?:필요한|중요한)\s?(?:것은|건)|핵심은|관건은", "글", 1),
    ("사람 글에 없는 은유", r"잠식|청사진|적신호|경고등|신호탄|움켜쥐|뿌리내리|짓누르", "글", 1),
    ("사람도 쓰는 은유 청구서·과실·주춧돌", r"청구서|과실[을이]|주춧돌|성적표|씨앗|짊어지", "글", 3),
    ("과제도 남아 있다·한계도 분명하다", r"과제도\s?(?:남아\s?있|남았|뚜렷)|한계도\s?분명|아쉬운\s?점도\s?있", "글", 1),
]
# 문장 하나에서 바로 보이는 낱말 티 (티 문장 비율의 아랫값을 센다)
SENT_TELL = (r"(?:필요한|중요한)\s?(?:것은|건)|핵심은|관건은|단순한?\s.{0,15}[을를]\s?넘어|에서의|으로의|에의|로부터의"
             r"|잠식|청사진|적신호|경고등|신호탄|움켜쥐|뿌리내리|짓누르|결국|이유(?:다|입니다|예요)[.!]?$|[가이] 아니라|것이 아니라"
             r"|(?:고|며|지만|면서|아서|어서|는데),|결론적으로|요약하면|정리하자면|종합하면|다양한|효과적|혁신적|획기적|원활한"
             r"|시사하는\s?바|자리매김|되어지|[을를]\s?가지고\s?있|할 때입니다|시점입니다|이는 .{0,30}보여"
             r"|과제도\s?(?:남아\s?있|남았|뚜렷)|한계도\s?분명|아쉬운\s?점도\s?있|요컨대|결론부터\s?(?:말씀드리면|말하자면|말하면)"
             r"|(?:진단|경고|분석|통계|현실|숫자|전망|결론)[은는이가]\s?(?:서늘하|아프|차갑|뜨겁|묵직하|섬뜩하)")
DUTY_END = r"(?:[가-힣]야\s?(?:한다|합니다|해요)|필요가\s?있(?:다|습니다|어요)|요구된다|요구됩니다)[.!]?$"
METAPHOR_ROOT = r"(쥐|쥘|움켜쥐|끌어안|짊어지|떠받치|붙들)"
INVISIBLE = {0x200B: "제로폭 공백", 0x200C: "제로폭 비결합자", 0x2060: "낱말 결합자", 0x2028: "줄 구분자", 0x2029: "문단 구분자",
             **{cp: "방향 제어 문자" for cp in (0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069)},
             0xFEFF: "BOM", 0x00AD: "소프트 하이픈", 0x00A0: "줄바꿈 없는 공백", 0x202F: "좁은 줄바꿈 없는 공백"}
NUM = r"\d+(?:[.,:/~-]\d+)*"
QUOTE = r"`[^`\n]+`|\"[^\"\n]+\"|“[^”\n]+”|(?<!\w)'[^'\n]+'(?!\w)|「[^」\n]+」"


def count(pat, text):
    return len(re.findall(pat, text, re.M))


def sentences(text):
    flat = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", flat) if len(s.strip()) >= 4]


def registers(text):
    ss = sentences(text)
    return Counter("합니다" if re.search(r"(?:니다|니까|십시오)[.?!]?$", s)
                   else "해요" if re.search(r"(?<![필중개수주소강동풍])요[.?!]?$", s)
                   else "한다" if re.search(r"다[.?!]?$", s) else "기타" for s in ss)


def numbers(text):
    return Counter(n.rstrip(".,").replace(",", "") for n in re.findall(NUM, text))


def dense(text):
    hits = []
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    for name, pat, unit, th in DENSE:
        n = max((count(pat, p) for p in paras), default=0) if unit == "문단" else count(pat, text)
        if n >= th:
            hits.append(f"{name}: {unit} {n}번 (문턱 {th})")
    ss = sentences(text)
    if len(ss) >= 10 and max(len(s) for s in ss) < 100:
        hits.append(f"100자 넘는 문장 없음: 문장 {len(ss)}개, 가장 긴 문장 {max(len(s) for s in ss)}자")
    duty = sum(1 for p in paras if sentences(p) and re.search(DUTY_END, sentences(p)[-1]))
    if duty >= 2:
        hits.append(f"당위로 끝나는 문단: {duty}개 (첫째를 빼고 당위 문장을 문단 앞·가운데로 옮긴다)")
    tail = text[int(len(text) * 0.7):]
    n = count(r"(?:^|[.!?]\s)(?:향후|앞으로는?|중?장기적으로는?)\s", tail)
    if n:
        hits.append(f"글 끝 30%의 문두 '향후·앞으로': {n}번")
    run = best = 0
    for s in ss:
        run = run + 1 if re.search(r"것이다[.!]?$|것입니다[.!]?$", s) else 0
        best = max(best, run)
    if best >= 3:
        hits.append(f"'~것이다' 종결 {best}번 이어짐")
    roots = Counter({"쥘": "쥐"}.get(m, m) for m in re.findall(METAPHOR_ROOT, text))
    hits += [f"같은 은유 낱말 '{r}' {k}번 (가장 나은 한 번만 남긴다)" for r, k in roots.items() if k >= 3]
    return hits


def invisible(text):
    found = [f"{name} {text.count(chr(cp))}개" for cp, name in INVISIBLE.items() if chr(cp) in text]
    tags = sum(1 for ch in text if 0xE0000 <= ord(ch) <= 0xE007F)
    if tags:
        found.append(f"숨은 태그 문자 {tags}개")
    if unicodedata.normalize("NFC", text) != text:
        found.append("분해된 한글(NFD)")
    return found


def tagged(text):
    ss = sentences(text)
    n = sum(1 for s in ss if re.search(SENT_TELL, s))
    return f"{n}/{len(ss)} ({n / len(ss):.0%})" if ss else "0/0"


def compare(before, after, keep=()):
    nb, na = numbers(before), numbers(after)
    qb, qa = Counter(re.findall(QUOTE, before)), Counter(re.findall(QUOTE, after))
    a, b = re.sub(r"\s+", " ", before).strip(), re.sub(r"\s+", " ", after).strip()
    sb, sa = set(sentences(before)), sentences(after)
    rb, ra = registers(before), registers(after)
    reg = []
    if rb and ra and rb.most_common(1)[0][0] != ra.most_common(1)[0][0]:
        reg.append("주된 말투가 바뀌었다")
    if rb["해요"] >= 3 and ra["해요"] < rb["해요"] / 2:
        reg.append("해요체 종결이 절반 밑으로 줄었다")
    ratio = len(b) / len(a) if a else 1
    lost = [w for w in keep if w in before and w not in after]
    return {
        "길이": f"{ratio:.0%}" + (" (절반 아래, 빠진 내용 확인)" if ratio < 0.5 else " (두 배 넘음, 보탠 내용 확인)" if ratio > 2 else ""),
        "지킬 낱말 빠짐(실패)": ", ".join(lost) or ("없음" if keep else "목록 없음"),
        "바뀐 글자": f"{1 - difflib.SequenceMatcher(None, a, b, autojunk=False).ratio():.0%}",
        "바뀐 문장": f"{sum(1 for s in sa if s not in sb)}/{len(sa)}",
        "낱말 티 문장": tagged(after),
        "숫자 생김(실패)": ", ".join(na - nb) or "없음",
        "숫자 빠짐(짝 문장 확인)": ", ".join(nb - na) or "없음",
        "인용 생김·빠짐": ", ".join(list(qa - qb) + list(qb - qa)) or "없음",
        "늘어난 꼴(다시 고친다)": ", ".join(f"{n} {count(p, before)}→{count(p, after)}" for n, p in GROW
                                   if count(p, after) > count(p, before)) or "없음",
        "줄어든 서법 표지(짝 문장 확인)": ", ".join(f"{n} {count(p, before)}→{count(p, after)}" for n, p in KEEP
                                         if count(p, after) < count(p, before)) or "없음",
        "말투(되돌린다)": ", ".join(reg) or "그대로",
        "보이지 않는 문자": ", ".join(invisible(after)) or "없음",
    }


def main():
    args = sys.argv[1:]
    keep = []
    if "--keep" in args:
        i = args.index("--keep")
        keep = [w.strip() for w in open(args[i + 1], encoding="utf-8-sig") if w.strip()]
        del args[i:i + 2]
    paths = args
    if not paths:
        sys.exit(__doc__)
    before = open(paths[0], encoding="utf-8-sig").read()
    print("## 원문")
    print(f"- 낱말 티가 걸린 문장: {tagged(before)}. 뼈대 티(30~34)는 이 검사로 잡히지 않으니 문장마다 따로 본다.")
    print("\n".join("- 문턱값을 넘은 꼴: " + h for h in dense(before)) or "- 문턱값을 넘은 꼴: 없음")
    results = [(p, compare(before, open(p, encoding="utf-8-sig").read(), keep)) for p in paths[1:]]
    if len(results) == 1:
        print("\n## 전후 대조")
        print("\n".join(f"- {k}: {v}" for k, v in results[0][1].items()))
    elif results:
        keys = list(results[0][1])
        print("\n## 판 비교\n")
        print("| 판 | " + " | ".join(keys) + " |")
        print("|---" * (len(keys) + 1) + "|")
        for p, r in results:
            print(f"| {p.replace(chr(92), '/').split('/')[-1]} | " + " | ".join(r[k] for k in keys) + " |")


if __name__ == "__main__":
    main()
