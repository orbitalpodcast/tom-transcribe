## Dependencies

* Python 2.7
* [Google Cloud SDK](https://cloud.google.com/sdk/docs/)
* [Google Cloud Python library](https://cloud.google.com/apis/docs/cloud-client-libraries)
* [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html)
* [TQDM](https://github.com/tqdm/tqdm#latest-pypi-stable-release)

## Configuration
* Config settings are all stored in a .ini file. Since PRAW already looks for one, we're just going to hitchhike and use a different section in theirs. This saves us having a second .ini file.
* Update praw.ini with
  * [your Reddit credentials](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)
    * This includes the name of the subreddit whose wiki you want your transcriptions uploaded to
  * your Google credentials [(this quickstart is handy!)](https://cloud.google.com/storage/docs/quickstart-gsutil)
* Update the template.txt file. This will be prepended to your transcribed audio before it's uploaded to the wiki.

## Usage

* Upload your audio files to your Google Cloud Storage bucket.
  * File names must be in the format episode-###.flac.
  * Files must be mono flac files. This hopefully won't be a requirement in the future.
  * Anything in there will get transcribed, so delete previously transcribed files. In the future, we'll check for wiki pages and ignore extant episodes.
* Run transcribe.py.
* Enjoy the progress bars.
* When it's complete, a local backup will be saved in the same directory the .py file was in, in a folder called backup.

## Reddit credentials

* You can either chose to have the bot run through your personal Reddit account or through it's own dummy account. Whichever account it uses, practically speaking, is not going to be able to use TFA. If you really, really want to use a TFA enabled account, let me know and I can add that capability later (or you can [just update your .ini file every time you use the program.](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#two-factor-authentication))