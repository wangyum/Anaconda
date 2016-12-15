var $, Backbone, BlazeDataSource, BlazeDataSources, RemoteDataSource, _, logger,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

$ = require("jquery");

_ = require("underscore");

Backbone = require("backbone");

logger = require("../../common/logging").logger;

RemoteDataSource = require("./remote_data_source");

BlazeDataSource = (function(superClass) {
  extend(BlazeDataSource, superClass);

  function BlazeDataSource() {
    this.update = bind(this.update, this);
    this.setup = bind(this.setup, this);
    this.destroy = bind(this.destroy, this);
    this.defaults = bind(this.defaults, this);
    return BlazeDataSource.__super__.constructor.apply(this, arguments);
  }

  BlazeDataSource.prototype.type = 'BlazeDataSource';

  BlazeDataSource.prototype.defaults = function() {
    return _.extend({}, BlazeDataSource.__super__.defaults.call(this), {
      expr: {},
      local: null,
      namespace: {}
    });
  };

  BlazeDataSource.prototype.destroy = function() {
    if (this.interval != null) {
      return clearInterval(this.interval);
    }
  };

  BlazeDataSource.prototype.setup = function(plot_view, glyph) {
    this.pv = plot_view;
    this.update();
    if (this.get('polling_interval')) {
      return this.interval = setInterval(this.update, this.get('polling_interval'));
    }
  };

  BlazeDataSource.prototype.update = function() {
    var data;
    data = JSON.stringify({
      expr: this.get('expr'),
      namespace: this.get('namespace')
    });
    return $.ajax({
      dataType: 'json',
      url: this.get('data_url'),
      data: data,
      xhrField: {
        withCredentials: true
      },
      method: 'POST',
      contentType: 'application/json'
    }).done((function(_this) {
      return function(data) {
        var colname, columns_of_data, data_dict, i, idx, len, orig_data, ref;
        columns_of_data = _.zip.apply(_, data.data);
        data_dict = {};
        ref = data.names;
        for (idx = i = 0, len = ref.length; i < len; idx = ++i) {
          colname = ref[idx];
          data_dict[colname] = columns_of_data[idx];
        }
        orig_data = _.clone(_this.get('data'));
        _.extend(orig_data, data_dict);
        _this.set('data', orig_data);
        return null;
      };
    })(this));
  };

  return BlazeDataSource;

})(RemoteDataSource.Model);

BlazeDataSources = (function(superClass) {
  extend(BlazeDataSources, superClass);

  function BlazeDataSources() {
    return BlazeDataSources.__super__.constructor.apply(this, arguments);
  }

  BlazeDataSources.prototype.model = BlazeDataSource;

  return BlazeDataSources;

})(Backbone.Collection);

module.exports = {
  Model: BlazeDataSource,
  Collection: new BlazeDataSources()
};
