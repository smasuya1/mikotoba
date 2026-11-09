import re
import os
import streamlit as st

st.title("御言葉")

# 選択肢と対応するファイル名
FILES = {
    "まとめ": "御言葉のまとめ.txt",
    "2025": "御言葉のまとめ2025.txt"
}

# 上部に切り替え用リンク風ボタン（ラジオボタンを横並びで配置）
selected_name = st.radio("表示するまとめを選択", list(FILES.keys()), horizontal=True)
selected_file = FILES[selected_name]

# ファイルを開いて全文を読み込む
text = ""
if os.path.exists(selected_file):
    try:
        with open(selected_file, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(selected_file, "r", encoding="cp932", errors="ignore") as f:
            text = f.read()
else:
    st.error(f"ファイルが見つかりません: {selected_file}")
    st.stop()

# 検索フォーム（file_pathごとに別キーにしておくことで切替時に自動リセット）
query = st.text_input("検索したい単語を入力", key=f"search_{selected_file}")

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