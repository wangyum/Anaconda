var ColumnDataSource, RemoteDataSource, _,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ColumnDataSource = require("./column_data_source");

RemoteDataSource = (function(superClass) {
  extend(RemoteDataSource, superClass);

  function RemoteDataSource() {
    this.defaults = bind(this.defaults, this);
    return RemoteDataSource.__super__.constructor.apply(this, arguments);
  }

  RemoteDataSource.prototype.type = 'RemoteDataSource';

  RemoteDataSource.prototype.defaults = function() {
    return _.extend({}, RemoteDataSource.__super__.defaults.call(this), {
      data: {},
      data_url: null,
      polling_interval: null
    });
  };

  return RemoteDataSource;

})(ColumnDataSource.Model);

module.exports = {
  Model: RemoteDataSource
};
