import datetime
import json
import os

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

EMAIL1 = os.environ.get('EMAIL1', 'julieyeqiu@gmail.com')
EMAIL2 = os.environ.get('EMAIL2')
TO_EMAILS = [EMAIL1, EMAIL2]
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'bookclub@blinkist.com')
EMAIL_FOOTER = os.environ.get('EMAIL_FOOTER', '')
EMAIL_HEADER = os.environ.get('EMAIL_HEADER', "<p>Here's your reading list for the week:</p>")
EMAIL_SUBJECT = os.environ.get('EMAIL_SUBJECT', 'Blinkist Book Club - Week #{}')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

READER_URL = 'https://www.blinkist.com/en/nc/reader/'
BOOK_URL = 'https://www.blinkist.com/en/books/'

BOOKS_BY_WEEK = [
    ['my-morning-routine-en', 'getting-things-done-en', 'tools-of-titans-en'],
    ['the-tipping-point-en', 'difficult-conversations-en', 'permission-marketing-en'],
    ['the-happiness-hypothesis-en', 'grain-brain-en', 'connected-crm-en'],
    ['seven-brief-lessons-on-physics-en', 'evicted-en', 'on-the-shortness-of-life-en'],
    ['never-eat-alone-en', 'buffett-en', 'thinking-fast-and-slow-en'],
    ['brief-answers-to-the-big-questions-en', 'value-proposition-design-en', 'the-life-changing-magic-of-tidying-up-en'],
    ['the-21-irrefutable-laws-of-leadership-en', 'my-age-of-anxiety-en', 'men-explain-things-to-me-en'],
    ['this-is-marketing-en', 'i-will-teach-you-to-be-rich-en', 'think-and-grow-rich-en'],
    ['turn-the-ship-around-en', 'the-most-important-thing-en', 'radical-candor-en'],
    ['leaders-eat-last-en', 'the-obstacle-is-the-way-en', 'educated-en'],
    ['how-to-talk-to-anyone-en', 'money-master-the-game-en', 'steve-jobs-en'],
    ['principles-en', 'the-little-book-that-still-beats-the-market-en', 'epic-content-marketing-en'],
    ['the-total-money-makeover-en', 'a-peoples-history-of-the-united-states-en', 'get-a-financial-life-en'],
    ['all-marketers-are-liars-en', 'deep-work-en', 'how-to-win-friends-and-influence-people-en'],
    ['the-22-immutable-laws-of-marketing-en', 'how-to-travel-the-world-on-50-dollars-a-day-en', 'the-power-of-habit-en'],
    ['tribe-of-mentors-en', 'salt-fat-acid-heat-en', 'she-comes-first-en'],
    ['designing-your-life-en', 'the-god-delusion-en', 'predictably-irrational-en'],
    ['millennial-money-en', 'a-short-history-of-nearly-everything-en', 'the-subtle-art-of-not-giving-a-f-star-ck-en'],
    ['the-distracted-mind-en', 'the-whole30-en', 'made-to-stick-en'],
    ['the-art-of-travel-en', 'option-b-en', 'mindset-en'],
    ['thrive-en', 'getting-more-en', 'to-sell-is-human-en'],
    ['the-truth-en', 'the-paleo-manifesto-en', 'give-and-take-en'],
    ['crossing-the-chasm-en', 'its-not-the-size-of-the-data-en', 'purple-cow-en'],
    ['hillbilly-elegy-en', 'the-economist-numbers-guide-en', 'nickel-and-dimed-en'],
    ['drive-en', 'eat-to-live-en', '12-rules-for-life-en'],
    ['the-effective-executive-en', 'start-with-why-en', 'antifragile-en'],
    ['sapiens-en', 'secrets-of-the-millionaire-mind-en', 'the-4-hour-body-en'],
    ['what-the-most-successful-people-do-before-breakfast-en', 'emotional-intelligence-en', 'a-slash-b-testing-en'],
    ['being-mortal-en', 'the-intelligent-investor-en', 'influence-en'],
    ['the-7-habits-of-highly-effective-people-en', 'girl-wash-your-face-en', 'the-lean-startup-en'],
    ['getting-to-yes-en', 'the-hard-thing-about-hard-things-en', 'dont-make-me-think-revisited-en'],
    ['high-performance-habits-en', 'rich-dad-poor-dad-en', 'zero-to-one-en'],
]


def create_html(group):
    msg = '<html><body>'
    msg += EMAIL_HEADER
    for idx, slug in enumerate(group):
        msg += '<p>{idx}. <a href="{book_url}{slug}">{name}</a></p>'.format(
                book_url=BOOK_URL,
                slug=slug,
                name=' '.join([word.title() for word in slug.split('-') if word != 'en']),
                idx=idx+1,
            )
    msg += EMAIL_FOOTER
    msg += '</body></html>'
    return msg


def email_edition(now=datetime.date.today()):
    start_date = datetime.date(2019, 1, 6)
    if (now - start_date).days % 7 == 0:
        edition = (now - start_date).days // 7 + 1
        return edition
    return None


def build_email(edition):
    group = BOOKS_BY_WEEK[edition - 1]
    mail = Mail(
        Email(EMAIL_FROM),
        EMAIL_SUBJECT.format(edition),
        Email(EMAIL1),
        Content("text/html", create_html(group))
    )
    if EMAIL2:
        mail.personalizations[0].add_to(Email(EMAIL2))
    return mail.get()


def build_email_no_helper(edition):
    return {
      "personalizations": [
        {
          "to": [
            {
              "email": TO_EMAILS,
            }
          ],
          "subject": EMAIL_SUBJECT.format(edition)
        }
      ],
      "from": {
        "email": EMAIL1,
      },
      "content": [
        {
          "type": "text/html",
          "value": create_html(group)
        }
      ]
    }

def _send_email(edition):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    data = build_email(edition)
    try:
        response = sg.client.mail.send.post(request_body=data)
        return 'Status {}'.format(response.status_code)
    except Exception as err:
        return 'SendGrid Request Error: {}'.format(err)
    return 'Error SHOULD NOT REACH THIS STATMENT'

def send_email(request):
    edition = request.args.get('send_edition', type=int)
    if edition:
        return _send_email(edition)

    if request.args.get('sunday', type=bool):
        edition = email_edition()
        if edition:
            return _send_email(edition)
        else:
            return 'No email for today'

    return 'No args specified. Provide either send_edition={edition} or sunday=true'
