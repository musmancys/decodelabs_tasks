import re

SUSPICIOUS_KEYWORDS = [
    "verify your account", "urgent action required", "click here",
    "confirm your identity", "account suspended", "limited time",
    "act now", "you have won", "update your payment", "password expires",
    "unusual activity", "wire transfer", "bypass procedure", "strictly confidential"
]

URL_SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"]

GENERIC_GREETINGS = ["dear customer", "dear user", "dear account holder"]


def find_urls(text):
    return re.findall(r'https?://\S+|www\.\S+', text)


def get_domain(url):
    url = re.sub(r'^https?://', '', url)
    return url.split('/')[0].lower()


def check_keywords(text):
    lowered = text.lower()
    return [word for word in SUSPICIOUS_KEYWORDS if word in lowered]


def check_urls(urls):
    flags = []
    for url in urls:
        domain = get_domain(url)
        if any(shortener in domain for shortener in URL_SHORTENERS):
            flags.append(f"'{url}' uses a URL shortener that hides the real destination")
        if re.match(r'^\d{1,3}(\.\d{1,3}){3}', domain):
            flags.append(f"'{url}' points directly to an IP address instead of a domain")
        if domain.count('-') >= 2:
            flags.append(f"'{url}' domain contains multiple hyphens, a common spoofing trick")
        if domain.count('.') >= 3:
            flags.append(f"'{url}' has a long nested subdomain that may bury the real root domain")
    return flags


def check_greeting(text):
    lowered = text.lower()
    return [greeting for greeting in GENERIC_GREETINGS if greeting in lowered]


def analyze_email(text):
    urls = find_urls(text)
    red_flags = []

    keyword_hits = check_keywords(text)
    if keyword_hits:
        red_flags.append("Suspicious keywords found: " + ", ".join(keyword_hits))

    red_flags.extend(check_urls(urls))

    if check_greeting(text):
        red_flags.append("Generic greeting used instead of the recipient's actual name")

    if len(red_flags) == 0:
        verdict = "Safe"
    elif len(red_flags) <= 2:
        verdict = "Suspicious"
    else:
        verdict = "Malicious"

    return red_flags, verdict


def read_email_input():
    print("Paste the email content below. Type END on a new line when finished.")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def main():
    print("=== Phantom Phishing Analysis ===")
    email_text = read_email_input()
    red_flags, verdict = analyze_email(email_text)

    print("\n--- Analysis Report ---")
    if red_flags:
        for flag in red_flags:
            print("-", flag)
    else:
        print("No red flags detected in this message.")

    print("\nFinal Verdict:", verdict)


if __name__ == "__main__":
    main()
