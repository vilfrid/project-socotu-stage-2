odoo.define('air_waybill.financial_column_toggle', function(require){
    "use strict";

    const ListRenderer = require('web.ListRenderer');
    const patch = require('web.utils').patch;

    patch(ListRenderer.prototype, 'air_waybill.financial_column_toggle', {
        _renderBody: function () {
            const $body = this._super.apply(this, arguments);

            // Vérifie si le premier record a hide_column_2 activé
            const hideColumn = this.state.data.length && this.state.data[0].hide_column_2;

            if (hideColumn) {
                this.$el.find('th:contains("Company"), td[data-name="column_2"]').hide();
            } else {
                this.$el.find('th:contains("Company"), td[data-name="column_2"]').show();
            }
            return $body;
        },
    });
});
