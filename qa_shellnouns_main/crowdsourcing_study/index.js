Survey.StylesManager.applyTheme("modern");

function download(filename, text) {
  var element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text)
  );
  element.setAttribute("download", filename);

  element.style.display = "none";
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

$(document).ready(function () {
  // load survey configuration and questions
  $.ajax({
    type: "GET",
    url: "./config/demo.json",
    crossDomain: true,
    success: function (data) {
      var survey = new Survey.Model(data);

      // scroll to top after clicking start and when changing pages
      survey.onStarted.add(function () {
        $("html, body").animate({ scrollTop: 0 }, "slow");
      });

      survey.onCurrentPageChanged.add(function () {
        $("html, body").animate({ scrollTop: 0 });
      });

      survey.onComplete.add(function (result) {
        download("result.json", JSON.stringify(result.data, null, 3));
      });

      $("#surveyElement").Survey({ model: survey });

      survey.setValue("batchNo", data.batchNo);

      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);
      const prolificId = urlParams.get("PROLIFIC_PID") || "TestID";
      const studyId = urlParams.get("STUDY_ID");
      const sessionId = urlParams.get("SESSION_ID");

      survey.setValue("prolificId", prolificId);
      survey.setValue("studyId", studyId);
      survey.setValue("sessionId", sessionId);
    },
  });
});
