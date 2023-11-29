const API_BASE_URL = process.env.NODE_ENV === 'production' ? 'https://backend.finance.iitmparadox.org' : 'http://localhost:5000';
const BILL_FORM_URL = process.env.NODE_ENV === 'production' ? 'https://finance.iitmparadox.org/bill-form' : 'http://localhost:8080/bill-form';

export default {
    API_BASE_URL,
    BILL_FORM_URL
};