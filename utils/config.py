USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
)
VIEWPORT = {'width': 1280, 'height': 720}
RECAPTCHA_IFRAME_SELECTOR = "iframe[title*='reCAPTCHA']"
RECAPTCHA_CHALLENGE_IFRAME_SELECTOR = "iframe[title='recaptcha challenge expires in two minutes']"
RECAPTCHA_CHECKBOX_SELECTOR = '.recaptcha-checkbox-border'
RECAPTCHA_AUDIO_BUTTON_SELECTOR = '#recaptcha-audio-button'
RECAPTCHA_VERIFY_BUTTON_SELECTOR = 'button#recaptcha-verify-button'
AUDIO_DOWNLOAD_LINK_SELECTOR = 'a.rc-audiochallenge-tdownload-link'
AUDIO_RESPONSE_INPUT_SELECTOR = 'input#audio-response'
VERIFY_BUTTON_SELECTOR = '.rc-button-default.goog-inline-block'
