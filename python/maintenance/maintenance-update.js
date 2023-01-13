const dateformat = require('dateformat');

/* ========= EDIT BELOW ========= */
// Time format example: 2021-09-22T03:30:00
const maintenance_start_time = '2022-05-18T20:00:00';
const maintenance_end_time = '2022-05-19T06:30:00';

/* ========= EDIT ABOVE ========= */

const applyIDLocalization = () => {
    dateformat.i18n = {
        dayNames: [
            "Sun",
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Minggu",
            "Senin",
            "Selasa",
            "Rabu",
            "Kamis",
            "Jumat",
            "Sabtu",
        ],
        monthNames: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni",
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember",
        ],
        timeNames: ["a", "p", "am", "pm", "A", "P", "AM", "PM"],
    };
}

const sg_start = `${dateformat(new Date(`${maintenance_start_time}+08:00`), 'dd mmmm, yyyy, dddd h:MM TT')} (GMT +8:00)`;
const sg_end = `${dateformat(new Date(`${maintenance_end_time}+08:00`), 'dd mmmm, yyyy, dddd h:MM TT')} (GMT +8:00)`;
const id_start_en = `${dateformat(new Date(`${maintenance_start_time}+09:00`), 'dddd, dd mmmm yyyy "at" H:MM')} (GMT +7)`;
const id_end_en = `${dateformat(new Date(`${maintenance_end_time}+09:00`), 'dddd, dd mmmm yyyy "at" H:MM')} (GMT +7)`;

applyIDLocalization();

const id_start = `${dateformat(new Date(`${maintenance_start_time}+09:00`), 'dddd, dd mmmm yyyy "pukul" H:MM')} WIB`;
const id_end = `${dateformat(new Date(`${maintenance_end_time}+09:00`), 'dddd, dd mmmm yyyy "pukul" H:MM')} WIB`;

console.log('>>> Copy and replace the value on template <<<');
console.log('');
console.log('== SG start & end ==');
console.log(sg_start, 'to', sg_end);
console.log('');
console.log('== ID start & end in English ==');
console.log(id_start_en, 'until', id_end_en);
console.log('');
console.log('== ID start & end ==');
console.log(id_start, 'hingga', id_end);
