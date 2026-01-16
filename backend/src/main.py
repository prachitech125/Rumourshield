import os
from dotenv import load_dotenv

from preprocess import clean_text
from predict import simple_rumour_signal, extract_factcheck_results
from factcheck_api import search_fact_checks


def main():
    load_dotenv()

    api_key = os.getenv("GOOGLE_FACTCHECK_API_KEY")

    print("\n🛡️ Rumourshield - Rumour Detection & Verification\n")

    user_text = input("Enter a post/news/blog text to check:\n> ").strip()
    if not user_text:
        print("\n❌ No input provided.")
        return

    cleaned = clean_text(user_text)

    # Step 1: Basic rumour signal
    signal = simple_rumour_signal(cleaned)

    print("\n✅ NLP Preprocessing Done")
    print(f"Prediction: {signal['label']}")
    print(f"Confidence: {signal['confidence']}")
    if signal["matched_keywords"]:
        print("Suspicious keywords:", ", ".join(signal["matched_keywords"]))

    # Step 2: Fact check verification
    if not api_key:
        print("\n⚠️ Google Fact Check API key not found.")
        print("Add it in .env file (use .env.example as reference).")
        return

    print("\n🔎 Checking Google Fact Check Tools API...")
    api_data = search_fact_checks(user_text, api_key)

    if "error" in api_data:
        print("\n❌ API Error:", api_data["error"])
        return

    factchecks = extract_factcheck_results(api_data)

    if not factchecks:
        print("\n⚠️ No verified fact-check results found for this claim.")
        print("Result: Unverified (Needs manual checking)")
        return

    print("\n✅ Fact-Check Results Found:")
    for i, item in enumerate(factchecks, start=1):
        print(f"\n{i}. Claim: {item['claim']}")
        print(f"   Publisher: {item['publisher']}")
        print(f"   Rating: {item['rating']}")
        print(f"   Source: {item['url']}")

    print("\n✅ Done! Rumourshield finished verification.\n")


if __name__ == "__main__":
    main()
