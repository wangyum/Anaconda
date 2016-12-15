var CellEditors, CellFormatters, Model, TableColumn, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Model = require("../../model");

CellEditors = require("./cell_formatters");

CellFormatters = require("./cell_formatters");

TableColumn = (function(superClass) {
  extend(TableColumn, superClass);

  function TableColumn() {
    return TableColumn.__super__.constructor.apply(this, arguments);
  }

  TableColumn.prototype.type = 'TableColumn';

  TableColumn.prototype.default_view = null;

  TableColumn.prototype.defaults = function() {
    return _.extend({}, TableColumn.__super__.defaults.call(this), {
      field: null,
      title: null,
      width: 300,
      formatter: new CellFormatters.String.Model(),
      editor: new CellEditors.String.Model(),
      sortable: true,
      default_sort: "ascending"
    });
  };

  TableColumn.prototype.toColumn = function() {
    return {
      id: _.uniqueId(),
      field: this.get("field"),
      name: this.get("title"),
      width: this.get("width"),
      formatter: this.get("formatter"),
      editor: this.get("editor"),
      sortable: this.get("sortable"),
      defaultSortAsc: this.get("default_sort") === "ascending"
    };
  };

  return TableColumn;

})(Model);

module.exports = {
  Model: TableColumn
};
