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
    $.getJSON('/stocks.json')
    .done( function(data){
      stocks = data;
    }).fail( function() {
      $('#indice').html("Sorry! Can't load stocks at the moment")
    })
  }

loadStocks();

  // The stocks are loaded when an event is triggered
  $("#content").on('click', '#indice a', function(e) {

    e.preventDefault();
    var indice = this.id.toUpperCase();

    var newContent = '';
    for (var i = 0; i < stocks[indice].length; i++) {
      // There will be a lot. Maybe this go in a scroll box?
      newContent += '<li><span class="stocks">' + stocks[indice][i].unique + '</span>';
      newContent += '<a href="placeholder.html#';
      newContent += stocks[indice][i].friendly.replace(/ /g, '-') + '">';
      newContent += stocks[indice][i].friendly + '</a></li>';
    }

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
