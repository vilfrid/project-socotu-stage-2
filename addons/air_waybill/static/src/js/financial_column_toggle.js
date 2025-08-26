/** @odoo-module **/
import { ListRenderer } from '@web/views/list/list_renderer';
import { patch } from '@web/core/utils/patch';

patch(ListRenderer.prototype, 'air_waybill.financial_column_toggle', {
    /**
     * Après le rendu du body, on cache/affiche la colonne 2
     */
    _renderBody() {
        const $body = this._super(...arguments);

        // Vérifie si le parent record a hide_column_2 = true
        if (this.state.model === 'air.waybill.line' && this.renderer.state) {
            const parentHide = this.renderer.state.context.hide_column_2;
            if (parentHide) {
                this.$el.find('th[data-name="column_2"], td[data-name="column_2"]').hide();
            } else {
                this.$el.find('th[data-name="column_2"], td[data-name="column_2"]').show();
            }
        }
        return $body;
    },
});
