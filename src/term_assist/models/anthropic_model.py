"""
Copyright 2024 Logan Kirkland

This file is part of term-assist.

term-assist is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

term-assist is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with
term-assist. If not, see <https://www.gnu.org/licenses/>.
"""

from anthropic import Anthropic

from term_assist.models.model import Model


class AnthropicModel(Model):
    def __init__(self, config, models, environment):
        super().__init__(config, models, environment)
        self.client = Anthropic()

    def message(self, prompt):
        message = self.client.messages.create(
            model=self.models["anthropic"][self.config["ai"]["model"]],
            max_tokens=self.config["ai"]["max_tokens"],
            temperature=self.config["ai"]["temperature"],
            system=self.config["ai"]["system_prompt"] + " " + self.environment,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text
