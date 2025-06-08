# mastodon ソートプログラム
import json

from mastodon import Mastodon

# 設定ファイルを読み込む
with open("config.json", "r") as f:
    config = json.load(f)

ACCESS_TOKEN = config["ACCESS_TOKEN"]
API_BASE_URL = config["API_BASE_URL"]

# 入力を受け取る
tag = input("検索するハッシュタグを入力してください（例: photo_contest2025）: ").strip().lstrip('#')
sort_key_input = input("ソート基準を選んでください（fav または boost）: ").strip().lower()

# ソートキーを決定
if sort_key_input == 'boost':
    sort_key = 'reblogs_count'
else:
    sort_key = 'favourites_count'  # デフォルトは fav

# Mastodon API に接続
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=API_BASE_URL
)

# ハッシュタグ付き投稿を取得
# 一回のリクエストでは40件までしか取得できないため、paginationを用いる。
toots = mastodon.fetch_remaining(
    first_page=mastodon.timeline_hashtag(tag, limit=40)
)

# 投稿をソート
sorted_toots = sorted(toots, key=lambda x: x[sort_key], reverse=True)

# 出力
print(f"\n--- #{tag} ランキング（{sort_key_input}順）---\n")

top_urls = []
for i, toot in enumerate(sorted_toots[:10], 1):
    favs = toot['favourites_count']
    boosts = toot['reblogs_count']
    url = toot['url']
    print(f"{i}. ❤️ {favs}  🔁 {boosts}")
    print(f"   URL: {url}\n")
    top_urls.append(url)

# 最後にURLだけ出力
print("--- 上位10件のURL一覧 ---")
for i, url in enumerate(top_urls, 1):
    print(f"{i}. {url}")