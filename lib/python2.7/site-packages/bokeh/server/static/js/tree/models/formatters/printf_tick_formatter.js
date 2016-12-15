var PrintfTickFormatter, SPrintf, TickFormatter, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

SPrintf = require("sprintf");

TickFormatter = require("./tick_formatter");

PrintfTickFormatter = (function(superClass) {
  extend(PrintfTickFormatter, superClass);

  function PrintfTickFormatter() {
    return PrintfTickFormatter.__super__.constructor.apply(this, arguments);
  }

  PrintfTickFormatter.prototype.type = 'PrintfTickFormatter';

  PrintfTickFormatter.prototype.format = function(ticks) {
    var format, labels, tick;
    format = this.get("format");
    labels = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = ticks.length; i < len; i++) {
        tick = ticks[i];
        results.push(SPrintf.sprintf(format, tick));
      }
      return results;
    })();
    return labels;
  };

  PrintfTickFormatter.prototype.defaults = function() {
    return _.extend({}, PrintfTickFormatter.__super__.defaults.call(this), {
      format: '%s'
    });
  };

  return PrintfTickFormatter;

})(TickFormatter.Model);

module.exports = {
  Model: PrintfTickFormatter
};
