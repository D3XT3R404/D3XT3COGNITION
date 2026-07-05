import requests


class CMSEngine:

    def run(self, target):

        findings = []

        confidence = {}

        try:

            url = f"https://{target}"

            r = requests.get(
                url,
                timeout=10
            )

            html = r.text.lower()

            if "wp-content" in html:

                findings.append(
                    "WordPress"
                )

                confidence[
                    "WordPress"
                ] = 95

            if "__next" in html:

                findings.append(
                    "NextJS"
                )

                confidence[
                    "NextJS"
                ] = 90

            if "drupal-settings-json" in html:

                findings.append(
                    "Drupal"
                )

                confidence[
                    "Drupal"
                ] = 90

        except:

            pass

        return {

            "detected":

                findings,

            "confidence":

                confidence

        }