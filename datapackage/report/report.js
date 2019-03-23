var width = $('#vis').width() - 50;
var reportSpec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v2.0.json',
    description: 'A Digital Awareness visualization.',
    height: 300, width: width,
    autosize: {
      type: "fit",
      contains: "padding"
    },
    data: {
      values: [
        {a: 'A', b: 28},
        {a: 'B', b: 55},
        {a: 'C', b: 43},
        {a: 'D', b: 91},
        {a: 'E', b: 81},
        {a: 'F', b: 53},
        {a: 'G', b: 19},
        {a: 'H', b: 87},
        {a: 'I', b: 52}
      ]
    },
    mark: 'bar',
    encoding: {
      x: {field: 'a', type: 'ordinal'},
      y: {field: 'b', type: 'quantitative'}
    }
  };

vegaEmbed('#vis', reportSpec);

$.ajax({
    dataType: "json",
    url: "data/summary.json",
    mimeType: "application/json",
    success: function(data) {
      $('[data]').each(function() {
        tgt = $(this).attr('data').split('.');
        obj = data;
        $.each(tgt, function() { obj = obj[this]; })
        $(this).html(obj);
      });
    }
  });
