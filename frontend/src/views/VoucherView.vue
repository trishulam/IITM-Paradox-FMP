<template>
    <div>
        <b-spinner variant="primary" v-if="loading"></b-spinner>
        <b-container v-if="!loading">

            <body id="divToPrint" class="cont">
                <header>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <img style="height: 100px; width: 100px;" src="../assets/paradox_new_logo.png" alt="Left Logo">
                        </div>
                        <div style="text-align: center;">
                            <h1>Expenditure Approval</h1>
                            <p style="text-align: center;">IITM Student Activities Trust<br>(IITM BS Degree
                                Programme)<br>Dean of Student Office<br>IIT
                                Madras<br>Chennai - 600036</p>
                        </div>
                        <div>
                            <img style="height: 100px; width: 110px;" src="../assets/stact.png" alt="Right Logo">
                        </div>
                    </div>
                    <hr style="border: 1px solid black; margin-top: 10px; margin-bottom: 20px;">
                </header>

                <div class="container">
                    <div style="font-size: 17px;" class="voucher-info">
                        <p><span style="font-size: 22px;">Voucher Number</span> <br>{{ voucherNumber }}</p>
                        <p><span style="font-size: 22px;">Date</span> <br>{{ billDetails.bill_date }}</p>
                        <p><span style="font-size: 22px;">Type</span> <br>{{ billDetails.bill_type }}</p>
                        <p><span style="font-size: 22px;">Department</span> <br>{{ billDetails.bill_department }}</p>
                    </div>

                    <div style="text-align: center;">
                        <h4>Vendor Details</h4>
                        <table>
                            <tr>
                                <th>Bill Number:</th>
                                <td>{{ billDetails.bill_number }}</td>
                            </tr>
                            <tr>
                                <th>Vendor Name:</th>
                                <td>{{ billDetails.vendor_name }}</td>
                            </tr>
                            <tr>
                                <th>Vendor Address:</th>
                                <td>{{ billDetails.vendor_address }}</td>
                            </tr>
                            <tr>
                                <th>GST Number:</th>
                                <td>{{ billDetails.gst_number }}</td>
                            </tr>
                        </table>
                        <br />
                        <div v-if="billDetails.bill_type == 'Vendor Payment'">
                            <h4>Vendor Bank Details</h4>
                            <table>
                                <tr>
                                    <th>Account Number</th>
                                    <td>{{ billDetails.acc_number }}</td>
                                </tr>
                                <tr>
                                    <th>Account Holder Name</th>
                                    <td>{{ billDetails.acc_holder_name }}</td>
                                </tr>
                                <tr>
                                    <th>Bank Name</th>
                                    <td>{{ billDetails.bank_name }}</td>
                                </tr>
                                <tr>
                                    <th>IFSC Code</th>
                                    <td>{{ billDetails.ifsc_code }}</td>
                                </tr>
                                <tr>
                                    <th>Branch Name</th>
                                    <td>{{ billDetails.bank_branch }}</td>
                                </tr>
                            </table>
                        </div>
                        <p style="margin: 20px auto 0px auto; text-align: center; font-size: 18px; font-weight: bold;">Bill
                            Description
                        </p>
                        <div>{{ billDetails.bill_description }}</div>
                        <table class="mt-2">
                            <tr>
                                <th>Bill Amount:</th>
                                <td>&#8377; {{ billDetails.bill_amount }} /-</td>
                            </tr>
                            <tr>
                                <th>Amount in Words:</th>
                                <!-- <td>{{ billDetails.bill_amount_in_words }}</td> -->
                                <td>{{ amountToWords }}</td>
                            </tr>
                        </table>
                        <!-- <p style="margin-top: 20px;"><em>Note: Kindly ensure the above details are correct and match the
                                invoice.</em></p> -->
                    </div>
                </div>
                <footer v-if="billDetails.bill_type == 'Vendor Payment'">
                <!-- <footer v-if="billDetails.bill_type == 'Student Reimbursement'"> -->
                    <div class="footer-container">
                        <b-row style="margin: 0">
                            <b-col>
                                <img height="75px" width="100px" src="../assets/pradeesh_sign.jpeg" />
                            </b-col>
                            <b-col>
                                <img height="75px" width="100px" src="../assets/vamsi_sign.jpeg" />
                            </b-col>
                            <b-col>

                            </b-col>
                            <b-col>

                            </b-col>
                        </b-row>
                        <b-row style="margin: 0">
                            <b-col>
                                <h5>Finance Core</h5>
                            </b-col>
                            <b-col>
                                <h5>Secretary</h5>
                            </b-col>
                            <b-col>
                                <h5>Faculty Advisor</h5>
                            </b-col>
                            <b-col>
                                <h5>Managing Trustee</h5>
                            </b-col>
                        </b-row>
                    </div>

                </footer>
            </body>
            <b-button v-if="!isButtonLoading" class="mt-1" variant="primary" @click="printDoc()">Approve & Print</b-button>
            <b-button v-if="isButtonLoading" class="mt-1" variant="primary" disabled>
                <b-spinner small type="grow"></b-spinner>
                Loading...
            </b-button>
        </b-container>
    </div>
</template>

<script>
import html2pdf from "html2pdf.js";
import axios from 'axios';
import { mapGetters } from 'vuex';
import config from '@/config.js'
import { ToWords } from 'to-words';

export default {
    name: 'VoucherView',
    components: {

    },
    data() {
        const toWords = new ToWords({
            localeCode: 'en-IN',
            converterOptions: {
                currency: true,
                ignoreDecimal: false,
                ignoreZeroCurrency: false,
                doNotAddOnly: false,
                currencyOptions: { // can be used to override defaults for the selected locale
                    name: 'Rupee',
                    plural: 'Rupees',
                    symbol: '₹',
                    fractionalUnit: {
                        name: 'Paisa',
                        plural: 'Paise',
                        symbol: '',
                    },
                }
            }
        });
        return {
            billDetails: {},
            lengthFcApproved: null,
            voucherNumber: null,
            loading: true,
            isButtonLoading: false,
            toWords: toWords
        };
    },
    computed: {
        ...mapGetters(['billId']),
        amountToWords() {
            return this.toWords.convert(this.billDetails.bill_amount);
        }
    },
    methods: {
        async coreApprove() {
            var formData = new FormData();
            formData.append('bill_id', this.billId);
            axios.put(`${config.API_BASE_URL}/bills/fc-approved`, formData,
                {
                    headers: {
                        'x-access-token': localStorage.getItem('token')
                    }
                })
                .then(() => {
                    this.$bvToast.toast(`Bill verified successfully`, {
                        title: 'Bill Verification',
                        variant: 'success',
                        solid: true
                    })
                    this.getAllScApprovedBills();
                    this.getFcApprovedBills();
                    this.verifyId = null
                    this.$nextTick(() => {
                        this.$bvModal.hide('verify-modal')
                    })
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        printDoc() {
            const content = document.getElementById('divToPrint');
            this.isButtonLoading = true;
            // Define the options for the PDF conversion
            const options = {
                margin: 0,
                filename: 'myfile.pdf',
                image: { type: 'jpeg', quality: 1 },
                html2canvas: { dpi: 192, letterRendering: true },
                jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' },
            };

            // Generate the PDF
            // html2pdf().set(options).from(content).save();
            html2pdf().set(options).from(content).outputPdf('blob')
            .then(async (pdf) => {
                await this.coreApprove();
                // Create a form data object and append the PDF file blob
                var formData = new FormData();
                formData.append('pdf', pdf, `${this.voucherNumber}.pdf`);
                formData.append('bill_id', this.billId);

                var emailFormData = new FormData();
                emailFormData.append('bill_number', this.billDetails.bill_number);
                emailFormData.append('bill_description', this.billDetails.bill_description);
                emailFormData.append('email', this.billDetails.poc_email);
                emailFormData.append('voucher_number', this.voucherNumber);


                await axios.post(`${config.API_BASE_URL}/send-accept-mail`, emailFormData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'x-access-token': localStorage.getItem('token')
                    },
                })
                    .then(async () => {
                        console.log('Email sent successfully');
                        await axios.post(`${config.API_BASE_URL}/upload-voucher`, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data',
                                'x-access-token': localStorage.getItem('token')
                            },
                        })
                            .then(() => {
                                this.$bvToast.toast(`Voucher generated successfully`, {
                                    title: 'Voucher Generation',
                                    variant: 'success',
                                    solid: true
                                })
                                this.$router.push('/dashboard');
                            })
                            .catch((error) => {
                                console.error(error);
                            });
                    });
            })
            .catch((error) => {
                console.error(error);
            });
        },

        async getBillDetails() {
            var formData = new FormData();

            formData.append("bill_id", this.billId);
            await axios.post(`${config.API_BASE_URL}/bills/get-bill`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.billDetails = response.data.bill;
                })
                .catch((error) => {
                    console.error(error);
                });
        },

        async getLengthFcApproved() {
            await axios.get(`${config.API_BASE_URL}/bills/get-len-all-fc-approved`, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.lengthFcApproved = response.data.bills;
                    const formattedVoucherLength = (this.lengthFcApproved + 1).toString().padStart(3, '0');
                    this.voucherNumber = `PA-${formattedVoucherLength}`;
                })
                .catch((error) => {
                    console.error(error);
                });
        }

    },
    async mounted() {
        await this.getBillDetails();
        await this.getLengthFcApproved();
        this.loading = false;
    }
}
</script>

<style scoped>
header {
    padding: 20px;
    padding-bottom: 10px;
    height: 200px;
}

header h1 {
    margin: 0;
    font-size: 36px;
    font-weight: bold;
}

header p {
    margin: 5px 0;
    font-size: 15px;
}

table {
    border-collapse: collapse;
    margin: auto;
}

th,
td {
    padding: 5px 10px;
    border: 1px solid #ccc;
}

th {
    font-weight: bold;
    text-align: right;
}

td {
    text-align: left;
}

.container {
    margin: auto;
}

@page {
    size: A4;
    margin: 0;
}

body {
    width: 210mm;
    /* A4 width */
    height: 290mm;
    /* A4 height */
    margin: auto;
    position: relative;
}

.footer-container {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: auto;
    /* Adjust this value to set the height of the footer */
    text-align: center;
    line-height: 50px;
    margin-bottom: 25px;
}

.voucher-info {
    text-align: center;
    display: flex;
    justify-content: space-between;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 20px;
    margin-bottom: 10px;
}

.voucher-info p {
    margin: 0;
}

.left {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.right {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.total {
    font-size: 1.5rem;
    margin-bottom: 10px;
}
</style>