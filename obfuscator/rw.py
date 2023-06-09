import pefile
import logger as lg

class Rw():
    
    def read(self, file_path):
        """Парсит структуру файла, и возвращает указатель на .text"""
        self.pe = pefile.PE(file_path)
        return self
    
        # imagebase Адрес базовой загрузки 40_00_00h для Win
        # va Адрес относительно начала виртуальной памяти 1000h
        # rva место выгрузки программы
        # va = imagebase + rva
        # raw = rva - sectionRVA + rawSection

    def codedata(self):
        # AddressOfEntryPoint if guaranteed to be the first byte executed.
        self.eop = self.pe.OPTIONAL_HEADER.AddressOfEntryPoint
        #print('entry point is %s'%(self.eop))
        self.code_section = None
        for section in self.pe.sections:
            if section.contains_rva(self.eop):
                self.code_section = section
        data = self.code_section.get_data(self.eop, self.code_section.SizeOfRawData)
        return data
    
    def set_eop(self, addr_offset):
        """Устанавливает новую точку входа"""
        self.pe.OPTIONAL_HEADER.AddressOfEntryPoint = self.eop + addr_offset

    def write(self, file_path, llist_code):
        """Записывает изменения в файл"""
        flat_code = bytearray()

        for node in llist_code.forwardn():
            flat_code.extend(node.bytes)
        self.pe.set_bytes_at_rva(self.eop, bytes(flat_code))
        lg.info('result written at:%s'%(file_path))
        self.pe.write(filename=file_path)

rw = Rw()