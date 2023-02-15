"""module for data preprocessing """
import os
import re

import extract_msg
import PyPDF2
from extract_msg import validation


class Preprocessor:
    """preprocessor class with constraints"""

    def __init__(self):
        """
        constraints
        """
        self.extractor = extract_msg
        self.filename = ""
        self.extract_directory = ""
        self.source_directory = ""
        self.__regex_patterns = [
            "amend",
            "replace",
            "return",
            "attached",
            "send rated proof",
            "remove",
            "update",
            "send us",
        ]

    def validate_file(self, source_dir, filename):
        """

        :param source_dir: input directory
        :param filename: filename
        :return: validation
        """
        self.source_directory = source_dir
        self.filename = filename
        results = validation.validate(os.path.join(source_dir, self.filename))
        return results["olefile"]["valid"]

    def pdf_extract(self, ext_dir, source_dir, filename):
        """

        :param ext_dir:extraction directory
        :param source_dir: input directory
        :param filename: filename
        :return: extracted txt file
        """
        self.extract_directory = ext_dir
        self.source_directory = source_dir
        self.filename = filename

        with open((os.path.join(self.source_directory, self.filename)), "rb") as pdf_file, open(
            (os.path.join(self.extract_directory, "message.txt")),
            "w",
        ) as text_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()

            for page_number in range(number_of_pages):
                page = read_pdf.getPage(page_number)
                page_content = page.extractText()
                # print(page_content)
                text_file.write(page_content)

        text_file.close()

    def download_all_attachments(self, ext_dir):
        """
        downloads all attachments and messages
        :param ext_dir: extraction directory
        :return:
        """
        self.extract_directory = ext_dir

        message = self.extractor.openMsg(os.path.join(self.source_directory, self.filename))
        # This will create a separate folder for each email inside the parent folder and save a text file with
        # email body content, also it will download all attachments inside this folder.`
        message.save(customPath=self.extract_directory, useMsgFilename=True)

    def extract_pdf_patterns(self):
        """
        :return: dict for extracted pdf patterns
        """
        results = {}
        for file in os.listdir(self.extract_directory):
            if file.endswith(".txt"):
                message_file = os.path.join(self.extract_directory, file)
                pattern = []

                with open(message_file) as file1:
                    for line in file1:
                        if line == "\n":
                            continue
                        for character in self.__regex_patterns:
                            if re.search(character, line.lower()):
                                pattern.append(line.strip("\n"))
                    results["pattern"] = pattern

                with open(message_file) as file1:
                    for line in file1:
                        if line == "\n":
                            continue
                        if re.search("^([^,]*):", line):
                            data = line.split(":")
                            keyy = data[0]
                            valuee = data[1]

                            if keyy in results.keys():

                                results[keyy] = results[keyy], valuee
                            else:
                                results[keyy] = valuee

        return results

    def extract_patterns(self):
        """
        :return: dict for extracted eml patterns
        """
        results = {}
        for __, directories, _ in os.walk(self.extract_directory):
            for directory in directories:
                if directory.endswith(self.filename.replace(".msg", "")):
                    message_file = os.path.join(self.extract_directory, directory, "message.txt")
                    pattern = []

                    with open(message_file) as file:
                        for line in file:
                            if line == "\n":
                                continue
                            for character in self.__regex_patterns:
                                if re.search(character, line.lower()):
                                    pattern.append(line.strip("\n"))
                        results["pattern"] = pattern

        return results

    def clean(self):
        """Cleaning the upload and extract directories"""
        for file_dir in os.listdir(self.extract_directory):
            os.remove(self.extract_directory + file_dir)
            # shutil.rmtree(self.extract_directory + file_dir)

        for files in os.listdir(self.source_directory):

            os.remove(os.path.join(self.source_directory, files))
            # shutil.rmtree(os.path.join(self.source_directory, f))
