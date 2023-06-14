from struct import unpack

marker_mapping = {
    0xFFC0: "SOF0",
    0xFFC1: "SOF1",
    0xFFC2: "SOF2",
    0xFFC3: "SOF3",
    0xFFC4: "DHT",
    0xFFC5: "SOF5",
    0xFFC6: "SOF6",
    0xFFC7: "SOF7",
    0xFFC8: "JPG",
    0xFFC9: "SOF9",
    0xFFCA: "SOF10",
    0xFFCB: "SOF11",
    0xFFCC: "DAC",
    0xFFCD: "SOF13",
    0xFFCE: "SOF14",
    0xFFCF: "SOF15",
    0xFFD0: "RST0",
    0xFFD1: "RST1",
    0xFFD2: "RST2",
    0xFFD3: "RST3",
    0xFFD4: "RST4",
    0xFFD5: "RST5",
    0xFFD6: "RST6",
    0xFFD7: "RST7",
    0xFFD8: "SOI",
    0xFFD9: "EOI",
    0xFFDA: "SOS",
    0xFFDB: "DQT",
    0xFFDC: "DNL",
    0xFFDD: "DRI",
    0xFFDE: "DHP",
    0xFFDF: "EXP",
    0xFFE0: "APP0",
    0xFFE1: "APP1",
    0xFFE2: "APP2",
    0xFFE3: "APP3",
    0xFFE4: "APP4",
    0xFFE5: "APP5",
    0xFFE6: "APP6",
    0xFFE7: "APP7",
    0xFFE8: "APP8",
    0xFFE9: "APP9",
    0xFFEA: "APP10",
    0xFFEB: "APP11",
    0xFFEC: "APP12",
    0xFFED: "APP13",
    0xFFEE: "APP14",
    0xFFEF: "APP15",
    0xFFF0: "JPG0",
    0xFFF1: "JPG1",
    0xFFF2: "JPG2",
    0xFFF3: "JPG3",
    0xFFF4: "JPG4",
    0xFFF5: "JPG5",
    0xFFF6: "JPG6",
    0xFFF7: "JPG7",
    0xFFF8: "JPG8",
    0xFFF9: "JPG9",
    0xFFFA: "JPG10",
    0xFFFB: "JPG11",
    0xFFFC: "JPG12",
    0xFFFD: "JPG13",
    0xFFFE: "COM",
    0xFF01: "TEM",
}


class JPEG:
    def __init__(self, image_file):
        self.path = image_file
        with open(image_file, "rb") as f:
            self.img_data = f.read()

    def decode(self):
        data = self.img_data
        marker_DQT_num = 0
        marker_DQT_size_max = 0
        marker_DHT_num = 0
        marker_DHT_size_max = 0
        file_markers_num = 0
        marker_EOI_content_after_num = 0
        marker_APP12_size_max = 0
        marker_APP1_size_max = 0
        marker_COM_size_max = 0
        file_size = len(data)
        # print(f"file_size = {file_size}")
        while True:
            try:
                (marker,) = unpack(">H", data[0:2])
            except Exception as e:
                pass
            marker_map = marker_mapping.get(marker)
            if marker_map != None:
                file_markers_num += 1
                if marker_map == "DQT":
                    marker_DQT_num += 1
                    (lenchunk,) = unpack(">H", data[2:4])
                    if lenchunk > marker_DQT_size_max:
                        marker_DQT_size_max = lenchunk
                    data = data[2 + lenchunk :]
                elif marker_map == "SOI":
                    data = data[2:]
                elif marker_map == "DHT":
                    marker_DHT_num += 1
                    (lenchunk,) = unpack(">H", data[2:4])
                    if lenchunk > marker_DHT_size_max:
                        marker_DHT_size_max = lenchunk
                    data = data[2 + lenchunk :]
                elif marker_map == "EOI":
                    rem = data[2:]
                    if len(rem) > marker_EOI_content_after_num:
                        marker_EOI_content_after_num = len(rem)
                    data = rem
                elif marker_map == "SOS":
                    data = data[-2:]
                elif marker_map == "APP12":
                    (lenchunk,) = unpack(">H", data[2:4])
                    if lenchunk > marker_APP12_size_max:
                        marker_APP12_size_max = lenchunk
                    data = data[2 + lenchunk :]
                elif marker_map == "APP1":
                    (lenchunk,) = unpack(">H", data[2:4])
                    if lenchunk > marker_APP1_size_max:
                        marker_APP1_size_max = lenchunk
                    data = data[2 + lenchunk :]
                elif marker_map == "COM":
                    (lenchunk,) = unpack(">H", data[2:4])
                    if lenchunk > marker_COM_size_max:
                        marker_COM_size_max = lenchunk
                    data = data[2 + lenchunk :]
                elif marker_map == "TEM":
                    data = data[2:]
                elif marker <= 0xFFD9 and marker >= 0xFFD0:
                    data = data[2:]
                elif marker <= 0xFFBF and marker >= 0xFF02:
                    (lenchunk,) = unpack(">H", data[2:4])
                    data = data[2 + lenchunk :]
                else:
                    (lenchunk,) = unpack(">H", data[2:4])
                    data = data[2 + lenchunk :]
            else:
                data = data[1:]
            if len(data) == 0:
                data_list = [
                    marker_EOI_content_after_num,
                    marker_DQT_num,
                    marker_DHT_num,
                    file_markers_num,
                    marker_DQT_size_max,
                    marker_DHT_size_max,
                    file_size,
                    marker_COM_size_max,
                    marker_APP1_size_max,
                    marker_APP12_size_max,
                ]
                return data_list


if __name__ == "__main__":
    print("This is a module.")
