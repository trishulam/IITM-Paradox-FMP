<template>
    <div>
        <h1>Processed Bills</h1>
        <div class="mt-5">
            <BillTable :bill_type="bill_type" />
        </div>
    </div>
</template>

<script>
import BillTable from '@/components/BillTable.vue';
export default {
    name: 'ProcessedBillsView',
    components: {
        BillTable
    },
    data() {
        return {
            bill_type: 'processed',
        };
    },
}
</script>

<style></style>