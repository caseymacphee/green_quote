$(function() {

  var stocks;
  $.ajax({beforeSend: function(xhr) {
    if (xhr.overrideMimeType) {
      // this prevents errors loading JSON
      xhr.overrideMimeType("application/json")
      }
    }
  });

  function loadStocks() {
    $.getJSON('/static/stocks.json')
     .done( function(data) {
        stocks = data;
        })
     .fail( function(d, textStatus, error) {
        $('#stocks').html("Sorry! Can't load stocks at the moment");
        /*
        console.log("getJSON failed, status: " +
              textStatus + ", error: "+error);
        */
    })
  }

loadStocks();

  // The stocks are loaded when an event is triggered
  $("#content").on('click', '.indices-button', function(e) {

    e.preventDefault();
    var indice = this.id;
    var newContent = '';

    // There will be a lot. Maybe this go in a scroll box?
    stock_list = stocks[indice]
    for( var stock_entry in stock_list) {
        company_info = stock_list[stock_entry]
        company_symbol = company_info[0].replace(":", "_");

        // build an 'li' for the company with a link
        newContent += "<li><a class='stocks' href='/lc/";
        newContent += company_symbol + "'>";
        newContent += company_info[1];
        newContent += "</a></li>";
    }

    $('#stocks').html('<h2>Index Companies</h2><ul>' + newContent + '</ul>');

    // swap visibility
    $('#indice a.current').removeClass('current');
    $(this).addClass('current')

    $('#company').text('');
  });


  function success(companydata) {
    // if the data is JSON, the HTML has to be built first to get back html
    var $company = $('#company');
    var newContent = '';

    for (var metric in companydata) {
      if (metric ==     "200-Day Moving Average" ||
          metric =="% Held by Insiders" ||
          metric =="% Held by Institutions" ||
          metric =="Trailing Annual Dividend Yield" ||
          metric =="Trailing Annual Dividend Yield %" ||
          metric =="5 Year Average Dividend Yield" ||
          metric =="Last Split Factor" ||
          metric =="Last Split Date") {
        continue
      } else {
        newContent += "<li>"+metric+":"+companydata[metric]+"<li>";
      }

    newContent = "<h2>Company Metrics</h2><ul>" + newContent + "<ul>";

    // if the data is html, it can just be written
    $company.html(newContent).find("li").hide().fadeIn(300);
  }

  // Click on one of the stocks to load a company
  $('#content').on('click', '#stocks li a', function (e) {
    e.preventDefault();

    // This is a slug, because the page doesn't exist.
    //  It is a URL that points to a Flask route which will return
    //  data about the code whose sym tag is on the slug
    var url_slug = this.href;

    // Flask does not like ':' in its URL's
    // The Flask route will look for underscore and convert to ':'
    // and stock symbols with NEVER have underscores, right?
    // the URL is now written with the underscore when it's created in
    // the onclick for the indice
    //url_slug = url_slug.replace(':','_');

    //var data = url_slug.split('/')

    // To load an HTML file off the disk, use the following 2 lines, assuming
    //  the title to be loaded matches.
    //load_title = load_title.replace('#', " #");
    //$('company').load(load_title);
    $.get(url_slug)
     .done(success
    ).fail(function() {
      alert("we failed this time")
    })
      //type: "GET",
      //dataType: "json",
      //url: data[0],
      //data: data[1],
      //timeout: 3000,
      //beforeSend: function() {
      //  $company.append('<div id="load">Loading</div>');
      //},
      //complete: function() {
      //  $("#loading").remove();
      //},
      //fail: function() {
      //  $company.html('<div class="loading">Please try again soon.</div>')
      //}
      //success: success

/*
    $.getJSON(url_slug)
     .done( function(data) {
        companydata = data;
        //
        // write code like in loadStocks() to display these company data metrics
        //

        })
     .fail( function(d, textStatus, error) {
      $company.html("Sorry! Can't load company data at the moment")

        // console.log("getJSON failed, status: " + textStatus + ", error: "+error);

     })
*/
    // swap visibility
    $('#indice a.current').removeClass('current');
    $(this).addClass('current');
  });


  // Click on something else
  $('nav a').on('click', function(e) {
    e.preventDefault();

    var dest_url = this.href;
    $('nav a.current').removeClass('current');
    $(this).addClass('current');

    $('#container').remove();
    $('#content').load(dest_url + '#container').hide().fadeIn('slow');
  });

});
