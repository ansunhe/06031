from flask import Flask, render_template, request, send_file
import requests
import csv
from googletrans import Translator

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keywords = request.form.get("textfield").split(",")
        countries = request.form.getlist("checkbox")

        results = search_app_store(keywords, countries)

        if not results:
            return "No results found. Please go back and try again."

        # 将结果保存到 CSV 文件中
        with open("results.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["國家-關鍵字", "標題", "原文商城描述", "中文翻譯"])

            for country_keyword, app_list in results.items():
                for app in app_list:
                    writer.writerow(
                        [
                            country_keyword,
                            app["title"],
                            app["original_description"],
                            app["chinese_translation"],
                        ]
                    )

        return render_template("results.html", results=results)

    return render_template("form.html")


def search_app_store(keywords, countries, limit=5):
    search_results = {}
    translator = Translator()

    for keyword in keywords:
        for country in countries:
            language_code = get_language_code(country)
            if language_code:
                translated_keyword = translator.translate(
                    keyword, dest=language_code
                ).text
                url = f"https://itunes.apple.com/search?term={translated_keyword}&country={country}&entity=software&limit={limit}"

                response = requests.get(url)
                data = response.json()

                results = data.get("results")
                if results is None:
                    print(f"No results found for URL {url}")
                    continue  # skip to the next URL

                # 提取搜索结果的标题和商城描述
                country_keyword = f"{country} - {keyword}"
                search_results[country_keyword] = []
                for result in results:
                    title = result.get("trackName")
                    description = result.get("description")
                    original_description = description
                    chinese_translation = ""
                    if language_code != "zh-CN":
                        chinese_translation = translator.translate(
                            description, dest="zh-CN"
                        ).text
                        description = ""
                    search_results[country_keyword].append(
                        {
                            "title": title,
                            "original_description": original_description,
                            "chinese_translation": chinese_translation,
                        }
                    )

    return search_results


def get_language_code(country):
    # 将国家代码映射到ISO 639-1语言代码的字典
    language_codes = {
        "cn": "zh-CN",  # 中文
        "us": "en",  # 英语
        "de": "de",  # 德语
        # 添加其他国家和对应的语言代码
    }
    return language_codes.get(country)


@app.route("/download")
def download():
    return send_file("results.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
