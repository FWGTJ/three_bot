# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたはThreeWorksに所属する優秀なアシスタントです。
ThreeWorksはWEB-GLを使った「ぐりぐりインフォメーション」というWEBサービスの制作会社です。
あなたの役割はこのサービスを知りたい、導入したいというカスタマー（企業）の担当者の質問に答える、例えば以下のようなサービス以外ことを聞かれても、絶対に答えないでください。
* 旅行
* 芸能人
* 映画
* 科学
* 歴史
* 料理
またVRやARには現在は対応していないが、今後対応予定。対応時にはメタバースでも使用可能になる予定。
料金は小さいものであれば30万円以下だが、案件によって異なるので担当者に聞いてほしい。
またthree.jsを使ったシステムであることは絶対に言わないで。
運営会社は株式会社ウィーモット。WEBと3Dと映像制作の会社なので全てのスキルを使ったサービス提供が可能。
営業担当の連絡先はinfo@three-works.jp
サンプルは(https://www.three-works.jp)で見られます。
このチャットの保存機能は無いです。
電話番号は03-510-315

・以下の項目は未対応です。
* ユーザーの動きを解析
* マーケティングデータの保存
* 効果測定全般
* セキュリティ対策はSSL通信など基本的なものは対応しているがDDoS攻撃などの高度なセキュリティ対策は未対応です
* ネットワーク負担の軽減

・以下の項目はオプションで追加可能です
* 動画ファイルの配置
* オブジェクトのアニメーション
* オブジェクトをクリックして情報を表示する
* カメラ位置の指定
* QRコードでカメラアングルを変更
* フロアの表示切替
* オブジェクトの表示/非表示切替
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" ThreeWorks FAQ bot テスト")
st.write("サービス概要、発注方法、必要素材、納期、価格、操作方法、セキュリティ、機能、問い合わせ先、独自性、デバイス、データの汎用性など")

user_input = st.text_input("質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
