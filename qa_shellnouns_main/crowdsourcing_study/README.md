# Demo Survey

This is a fully functioning demo of the main survey. To launch it you need to start a local server
and open index.html.

With Python:

1. `cd` to the/path/of/qa_shellnouns_main/crowdsourcing_study and run `python -m http.server`
2. Open <http://localhost:8000/> in your browser

In VS Code:

With the [LiveServer](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
extension installed, open index.html and click on the "Go Live" button in the bottom status bar.

The survey consists of 3 truncated test articles. After completion, the results are downloaded as a
JSON file to your hard drive. In the real study, crowdworkers had to complete 10 articles, and the
results were saved to a Firebase realtime database.
