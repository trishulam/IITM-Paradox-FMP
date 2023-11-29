<template>
    <div>
        <h1>Pending Bills</h1>
        <div class="mt-5">
            <BillTable :bill_type="bill_type" />
        </div>
    </div>
</template>

<script>
import BillTable from '@/components/BillTable.vue';
export default {
    name: 'PendingBillsView',
    components: {
        BillTable
    },
    data() {
        return {
            bill_type: 'pending',
        };
    },
}
</script>