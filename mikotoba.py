import re
import streamlit as st

st.title("御言葉")

# 表示したい長文（ファイルから読み込むことも可能）
# ファイル名（文字コード UTF-8 を指定）
file_path = "御言葉のまとめ.txt"

# ファイルを開いて全文を読み込む
# UTF-8 で開き、ダメなら cp932 で開く（自動判定）
try:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="cp932", errors="ignore") as f:
        text = f.read()

# 検索フォーム
query = st.text_input("検索したい単語を入力")

if query:
    # 検索キーワードが出現する箇所を特定
    matches = list(re.finditer(re.escape(query), text, re.IGNORECASE))
    count = len(matches)

    if count > 0:
        st.success(f"{count} 件見つかりました")

        # ジャンプ用ボタン（リンク）を並べる
        links = [f'<a href="#match_{i+1}">[{i+1}件目へジャンプ]</a>' for i in range(count)]
        st.markdown(" ".join(links), unsafe_allow_html=True)

        # テキスト内の該当箇所にIDとハイライトを付与
        def highlight(match, idx=[0]):
            idx[0] += 1
            return f'<span id="match_{idx[0]}" style="background-color: #ffeb3b; color: black; font-weight: bold;">{match.group(0)}</span>'

        highlighted_text = re.sub(re.escape(query), highlight, text, flags=re.IGNORECASE)
        # 改行をHTML用に変換して表示
        st.markdown(highlighted_text.replace("\n", "<br>"), unsafe_allow_html=True)
    else:
        st.warning("見つかりませんでした。")
        st.write(text)
else:
    st.write(text)