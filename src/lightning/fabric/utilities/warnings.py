# Copyright The Lightning AI team.
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
"""Warning-related utilities."""
import warnings
import textwrap
from typing import Optional, Any, Type

from lightning.fabric.utilities.rank_zero import LightningDeprecationWarning

# enable our warnings
warnings.simplefilter("default", category=LightningDeprecationWarning)


class PossibleUserWarning(UserWarning):
    """Warnings that could be false positives."""


def _format_warning(warning: Warning, category: Type[Warning], filename: str, lineno: int, line: Optional[Any] = None) -> str:
    lines = textwrap.wrap(f"{category.__name__}: {warning}", width=100)
    message = "\n".join(lines)
    message = textwrap.indent(message, prefix=" " * 4)
    return f"{filename}:{lineno}:\n{message}\n"


warnings.formatwarning = _format_warning
