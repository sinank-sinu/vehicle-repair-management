/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.get_top_repairs = publicWidget.Widget.extend({
    selector: '.top_repairs',
    async willStart()
    {
        const result = await rpc('/repairs', {});

        if (result && result.repairs)
        {
            const data = result.repairs;
            const chunkSize = 4;
            const chunks = [];
            for (let i = 0; i < data.length; i += chunkSize) {
                chunks.push(data.slice(i, i + chunkSize));
            }
            if (chunks.length > 0)
            {
                chunks[0].is_active = true;
            }
            this.chunks = chunks;
        }
    },
    start()
    {
        if (this.chunks)
        {
            const unique_id = "tempId_" + Math.random();
            this.$target.empty().html(
                renderToElement('vehicle_repair_management.category_data',
                    {chunks: this.chunks, carousel_id: unique_id}));
        }
    },
});
