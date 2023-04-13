import pefile

class Rw():
    
    def read(self, file_path):
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
        print('entry point is %s'%(self.eop))
        self.code_section = None
        for section in self.pe.sections:
            if section.contains_rva(self.eop):
                self.code_section = section
        data = self.code_section.get_data(self.eop, self.code_section.SizeOfRawData)
        return data
    
    def set_eop(self, addr_offset):
        self.pe.OPTIONAL_HEADER.AddressOfEntryPoint = self.eop + addr_offset

    def write(self, file_path, llist_code):
        flat_code = bytearray()

        for node in llist_code.forwardn():
            flat_code.extend(node.bytes)
        flat_code.append(90)
        #print(flat_code)
        self.pe.set_bytes_at_rva(self.eop, bytes(flat_code))
        #print(self.code_section.get_data(self.eop, self.code_section.SizeOfRawData))
        print('result written at:%s'%(file_path))
        self.pe.write(filename=file_path)

rw = Rw()