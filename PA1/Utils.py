import re
import email
import base64
import quopri

class utils(object):
	def __init__(self, label, raw_file):
		print('the label is: ')
		self.label = label
		self.raw_file = raw_file
		self.message = email.message_from_file(raw_file)
		self.tokens = self._get_tokens()

	
	def label(self):
		return self.label

	
	def raw_file(self):
		return self.raw_file

	
	def message(self):
		return self.message

	
	def tokenized(self):
		return self.tokens

	
	def _clean_string(self, string):
		clean_text = re.sub(r'<.*?>', ' ', string)
		return clean_text
		
	def _find_match(self, string):
		if not string:
			return []

		s = re.split(r'\s', string)
		r = re.compile(r'^[a-zA-Z]+[\.\,]?$')

		matches = list(filter(r.match, s))
		return [re.sub(r'\,|\.', '', m) for m in matches]
				
	def _get_subject_tokens(self):
		subject = self.message.get('subject')
		if not subject:
			return []
			
		subject = self.message.get('subject').lower()
		subject = self._clean_string(subject)

		return self._find_match(subject)
		
	
	def _get_body_tokens(self):
		payloads = self._get_payloads(self.message)

		tokens = []
		for payload in payloads:
			tokens += self._find_match(self._clean_string(payload.lower()))
		
		return tokens
	
	def _get_payloads(self, message):
		payloads = []
		
		if message.is_multipart():
			for part in message.walk():
				sub_part_payload = part.get_payload()
				if isinstance(sub_part_payload, list):
					for s in sub_part_payload:
						payloads += self._get_payloads(s)
				else:
					payloads += self._get_payloads(part)
					
		else:
			content_type = message.get_content_type().lower()
			content_disposition = str(message.get('Content-Disposition'))
			transfer_encoding = message.get('content-transfer-encoding', '').lower()
			
			if 'text' in content_type and 'attachment' not in content_disposition:
				s = message.get_payload().strip()
				
				if transfer_encoding == 'base64' and ' ' not in s:
					s = base64.b64decode(s).decode('latin-1')
					
				if transfer_encoding == 'quoted-printable':
					s = s.encode('ascii', errors='ignore').decode()
					s = quopri.decodestring(s).decode('latin-1')
				
				payloads.append(s)
		
		return payloads
	
	
	def _get_tokens(self):
		tokens = self._get_subject_tokens() + self._get_body_tokens()
		# Gives subject and message body
		return tokens
