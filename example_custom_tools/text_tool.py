# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example custom text processing tool for ADK."""

from __future__ import annotations


def count_words(text: str) -> int:
  """Count the number of words in a text.

  Args:
    text: The text to analyze

  Returns:
    The number of words in the text.
  """
  return len(text.split())


def reverse_text(text: str) -> str:
  """Reverse the given text.

  Args:
    text: The text to reverse

  Returns:
    The reversed text.
  """
  return text[::-1]


def to_uppercase(text: str) -> str:
  """Convert text to uppercase.

  Args:
    text: The text to convert

  Returns:
    The text in uppercase.
  """
  return text.upper()


def to_lowercase(text: str) -> str:
  """Convert text to lowercase.

  Args:
    text: The text to convert

  Returns:
    The text in lowercase.
  """
  return text.lower()
