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
      console.log(stocks.length)
      console.log(typeof(stocks))
      console.log(stocks)
    }).fail( function(d, textStatus, error) {
      $('#stocks').html("Sorry! Can't load stocks at the moment");
      console.log("getJSON failed, status: " +
            textStatus + ", error: "+error);
    })
  }

loadStocks();

  // The stocks are loaded when an event is triggered
  $("#content").on('click', '.indices-button', function(e) {

    e.preventDefault();
    var indice = this.id;

    var newContent = '';
    key_list = Object.keys(stocks[indice])


    var company_dict = stocks[indice]
    for (var company in company_dict){
        attribute_array = company_dict[company]
        newContent += '<li><span class="stocks">' + attribute_array[0] + '</span>';
        newContent += '<a href="placeholder.html#';
        //newContent += stocks[indice][i][1] + '">';
        newContent += attribute_array[1] + '</a></li>';
    }
    // There will be a lot. Maybe this go in a scroll box?

    $('#stocks').html('<ul>' + newContent + '<ul>');

    $('#indice a.current').removeClass('current');
    $(this).addClass('current')

    $('#company').text('');
  });


  // Click on one of the stocks to load a company
  $('#content').on('click', '#indice li a', function (e) {
    e.preventDefault();
    var load_title = this.href;

    load_title = load_title.replace('#', " #");
    $('company').load(load_title);

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
