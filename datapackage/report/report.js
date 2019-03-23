var width = $('#vis').parent().width() - 50;
var reportSpec = {
    $schema: 'https://vega.github.io/schema/vega-lite/v2.0.json',
    description: 'A Digital Awareness visualization.',
    height: 300, width: 80,
    // width: width,
    // autosize: {
    //   type: "fit",
    //   contains: "padding",
    //   resize: true
    // },
    data: { url: 'data/stats.json' },
    transform: [
      { calculate: "datum.type == 1 ? 'Risky' : 'Verified'", "as": "class" }
    ],
    spacing: 0,
    mark: 'bar',
    encoding: {
      column: {field: 'date', type: 'ordinal'},
      x: {
        field: 'class',
        type: 'nominal',
        scale: { rangeStep: 12},
        axis: { title: ""}
      },
      y: {
        aggregate: 'sum',
        field: 'hits',
        type: 'quantitative',
        axis: { title: 'Visits', grid: false }
      },
      color: {
        field: "class",
        type: "nominal",
        scale: {range: ["#DA3832", "#659CCA"]}
      }
    },
    config: {
      view: {"stroke": "transparent"},
      axis: {"domainWidth": 1},
      style: {"cell": {"stroke": "transparent"}}
    }
  };

$.ajax({
  dataType: "json",
  url: "data/stats.json",
  mimeType: "application/json",
  success: function(data) {
    reportSpec.data.values = data;
    vegaEmbed('#vis', reportSpec);
  }
});

function getTargetMarket(attr, obj) {
  tgt = attr.split('.');
  $.each(tgt, function() { obj = obj[this]; });
  return obj;
}

$.ajax({
  dataType: "json",
  url: "data/summary.json",
  mimeType: "application/json",
  success: function(data) {

    $('[data]').each(function() {
      var attr = $(this).attr('data');
      $(this).html(getTargetMarket(attr, data));
    });

    $('[data-list]').each(function() {
      var attr = $(this).attr('data-list');
      var $el = $(this);
      $.each(getTargetMarket(attr, data), function() {
        $el.append('<li>' + this + '</li>');
      });
    });

  }
});
